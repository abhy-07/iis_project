# Selection and transition rules

package storyteller

import java.io.File
import com.google.gson.Gson

private val gson = Gson()

fun loadStory(storyId: String): Story {
    StoryContext.storyCache[storyId]?.let { return it }

    val path = "data/processed/stories/$storyId.json"
    val json = File(path).readText()
    val story = gson.fromJson(json, Story::class.java)
    StoryContext.storyCache[storyId] = story
    return story
}

fun selectStory(mood: String, emotion: String): String {
    // very simple version; replace with your rules
    return when {
        mood in listOf("tired", "comfort-seeking", "sad") || emotion == "sad" ->
            "lantern_keeper"
        mood in listOf("excited", "happy", "energized") || emotion in listOf("happy", "surprised") ->
            "stardust_arena"
        else ->
            "abandoned_station"
    }
}

fun pickSceneTemplate(scene: Scene, emotion: String): String {
    return scene.templates[emotion] ?: scene.templates["neutral"] ?: scene.description
}

fun findScene(story: Story, sceneId: String): Scene? {
    return story.scenes.firstOrNull { it.id == sceneId }
}
