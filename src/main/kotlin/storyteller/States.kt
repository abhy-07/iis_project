# FSM skeleton (states)
package storyteller

import furhatos.flow.kotlin.*

val Idle: State = state {
    onEntry {
        goto(Greeting)
    }
}

val Greeting: State = state {
    onEntry {
        furhat.say("Hello, I’m your interactive storyteller.")
        goto(CollectProfile)
    }
}

val CollectProfile: State = state {
    onEntry {
        furhat.ask("How are you feeling right now? For example, tired, happy or neutral?")
    }

    onResponse {
        // TODO: map response to StoryContext.userMood
        StoryContext.userMood = "neutral" // placeholder
        goto(StorySelection)
    }
}

val StorySelection: State = state {
    onEntry {
        val storyId = selectStory(StoryContext.userMood, StoryContext.lastEmotion)
        StoryContext.currentStoryId = storyId
        StoryContext.currentSceneId = when (storyId) {
            "lantern_keeper"   -> "lk_intro"
            "stardust_arena"   -> "sa_intro"
            "abandoned_station"-> "at_intro"
            else               -> "at_intro"
        }
        goto(LoadScene)
    }
}

val LoadScene: State = state {
    onEntry {
        val storyId = StoryContext.currentStoryId ?: return@onEntry goto(StorySelection)
        val sceneId = StoryContext.currentSceneId ?: return@onEntry goto(StorySelection)

        val story = loadStory(storyId)
        val scene = findScene(story, sceneId) ?: return@onEntry goto(StorySelection)

        val text = pickSceneTemplate(scene, StoryContext.lastEmotion)
        furhat.say(text)

        if (scene.options.isEmpty()) {
            goto(StoryEnd)
        } else {
            goto(GetUserInput)
        }
    }
}

val GetUserInput: State = state {
    onEntry {
        furhat.ask("What would you like to do next?")
    }

    onResponse {
        // TODO: map response to StoryContext.lastIntent + an option id
        // For now, just go to DecideNextState
        goto(DecideNextState)
    }
}

val DecideNextState: State = state {
    onEntry {
        val storyId = StoryContext.currentStoryId ?: return@onEntry goto(StorySelection)
        val sceneId = StoryContext.currentSceneId ?: return@onEntry goto(StorySelection)
        val story = loadStory(storyId)
        val scene = findScene(story, sceneId) ?: return@onEntry goto(StorySelection)

        // TODO: implement proper intent & option handling
        // For now: pick first option if exists
        val next = scene.options.firstOrNull()?.nextScene

        if (next == null) {
            goto(StoryEnd)
        } else {
            StoryContext.currentSceneId = next
            goto(LoadScene)
        }
    }
}

val StoryEnd: State = state {
    onEntry {
        furhat.say("That was the end of this story.")
        goto(AskContinue)
    }
}

val AskContinue: State = state {
    onEntry {
        furhat.ask("Do you want another story, or do you want to stop?")
    }

    onResponse {
        // TODO: map response to continue/change_story/quit
        // Placeholder: always continue with new story
        goto(StorySelection)
    }
}

val Goodbye: State = state {
    onEntry {
        furhat.say("Goodbye!")
        goto(Idle)
    }
}
