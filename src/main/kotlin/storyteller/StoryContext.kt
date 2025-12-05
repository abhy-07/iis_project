# Shared variables

package storyteller

data class Story(
    val id: String,
    val name: String,
    val genre: String,
    val targetMoods: List<String>,
    val scenes: List<Scene>
)

data class Scene(
    val id: String,
    val description: String,
    val templates: Map<String, String>,
    val options: List<SceneOption>
)

data class SceneOption(
    val id: String,
    val text: String,
    val nextScene: String
)

object StoryContext {
    var currentStoryId: String? = null
    var currentSceneId: String? = null
    var lastEmotion: String = "neutral"
    var lastIntent: String = "continue"
    var userMood: String = "neutral"

    // cache loaded stories if you want
    val storyCache: MutableMap<String, Story> = mutableMapOf()
}
