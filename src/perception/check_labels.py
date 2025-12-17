import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Point to the training data
DATA_DIR = '../../data/fer2013/train'

if not os.path.exists(DATA_DIR):
    print("❌ Error: Can't find data folder.")
else:
    datagen = ImageDataGenerator(rescale=1./255)
    gen = datagen.flow_from_directory(
        DATA_DIR,
        target_size=(48, 48),
        class_mode='categorical',
        shuffle=False
    )
    
    print("\n✅ THE MODEL LEARNED THIS ORDER:")
    print(gen.class_indices)
    
    # Invert it so we can copy-paste into our demo
    labels = list(gen.class_indices.keys())
    print("\nPaste this list into your custom_demo.py:")
    print(f"EMOTION_LABELS = {labels}")