# Entry point
package storyteller

import furhatos.skills.Skill
import furhatos.flow.kotlin.Flow
import furhatos.flow.kotlin.FlowControlRunner

class StorySkill : Skill() {
    override fun start(flow: FlowControlRunner<Flow>) {
        flow.goto(Idle)
    }
}

fun main(args: Array<String>) {
    Skill.main(args)
}
