import os
import numpy as np
import tensorflow as tf
from sklearn.utils import class_weight
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization, Input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping

# --- 1. CONFIGURATION ---
# ONLY using the standard Kaggle Dataset
DATASET_DIR = '../../data/fer2013/train' 
VAL_DIR = '../../data/fer2013/test'

IMG_SIZE = (48, 48)
BATCH_SIZE = 64
EPOCHS = 100  # As requested

# --- 2. VERIFY PATHS ---
if not os.path.exists(DATASET_DIR):
    print(f"❌ ERROR: Could not find FER-2013 at {DATASET_DIR}")
    exit()

print(f"✅ Found FER-2013. Training for {EPOCHS} epochs...")

# --- 3. DATA GENERATORS ---
# We use aggressive augmentation to prevent overfitting during the long 100 epoch run
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=15,      
    width_shift_range=0.1,  
    height_shift_range=0.1, 
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)

print("--- Loading Training Data ---")
train_generator = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    color_mode='grayscale',
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True
)

print("--- Loading Validation Data ---")
val_gen = ImageDataGenerator(rescale=1./255).flow_from_directory(
    VAL_DIR,
    target_size=IMG_SIZE,
    color_mode='grayscale',
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

# --- 4. CALCULATE CLASS WEIGHTS (Critical for Sadness) ---
print("Calculating weights to fix class imbalance...")
class_weights_array = class_weight.compute_class_weight(
    class_weight='balanced',
    classes=np.unique(train_generator.classes),
    y=train_generator.classes
)
weights_dict = {i: w for i, w in enumerate(class_weights_array)}

# MANUAL BOOST: Force the model to care about SADNESS
# usually index 5 or 4. We find it dynamically.
sad_index = train_generator.class_indices.get('sad')
if sad_index is not None:
    print(f"Refining weights: Boosting 'sad' (Index {sad_index}) by 2x...")
    weights_dict[sad_index] *= 2.0 
else:
    print("⚠️ Warning: Could not find 'sad' class folder.")

# --- 5. MODEL ARCHITECTURE ---
model = Sequential([
    Input(shape=(48, 48, 1)),

    # Block 1
    Conv2D(32, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(32, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.2),

    # Block 2
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.2),

    # Block 3
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.2),

    # Block 4 (Deep features)
    Conv2D(256, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.2),

    # Classifier
    Flatten(),
    Dense(256, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),
    Dense(7, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# --- 6. TRAIN ---
callbacks = [
    # Slow down learning if we get stuck
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=4, verbose=1),
    # Stop if we don't improve for 15 epochs (saves time)
    EarlyStopping(monitor='val_loss', patience=15, verbose=1, restore_best_weights=True)
]

print(f"\n🚀 Starting Training on {train_generator.samples} images...")

# Since we use standard flow_from_directory, we can pass class_weight directly
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=val_gen,
    validation_steps=val_gen.samples // BATCH_SIZE,
    class_weight=weights_dict, 
    callbacks=callbacks
)

# --- 7. SAVE ---
save_name = 'my_emotion_model_v3.keras' # Version 3
model.save(save_name)
print(f"✅ Model saved as '{save_name}'")