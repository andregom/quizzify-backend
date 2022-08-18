import gradio as gr

from models.t5.execution.prediction import generate_question_from



context = gr.inputs.Textbox(
    lines=5, placeholder="Enter paragraph/context here...")
answer = gr.inputs.Textbox(lines=3, placeholder="Enter answer/keyword here...")
question = gr.outputs.Textbox(type="auto", label="Question")


def generate_question(context, answer):
    return generate_question_from(context, answer)


iface = gr.Interface(
    fn=generate_question,
    inputs=[context, answer],
    outputs=question)
iface.launch(debug=False)
