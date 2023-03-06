import gradio as gr
import openai
from reportlab.pdfgen import canvas

# FUNCTION


def storyGPT(key, name, situation, direction):
    messages = [{"role": "system", "content": "You are a inspiring storyteller and therapist who understand young people and students' struggle."},
                {"role": "user", "content": "Write the first part amongst 5 of a story about " + name + "who is "+situation+". Include a bold heading above the top starting with 'First part:'. Limit your answer to 4 sentences or less."}]

    openai.api_key = key
    first_part_story = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages)

    system_message = first_part_story["choices"][0]['message']
    messages.append(system_message)

    for i in ["Second"]:
        new_story_first_half = {
            "role": "user", "content": f"Write the {i} part of the story among 5 continuing from the previous part. Include a bold heading above the top starting with '{i} part:'. Limit your answer to 4 sentences or less."}
        messages.append(new_story_first_half)
        story = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages)
        system_message = story["choices"][0]["message"]
        messages.append(system_message)

    for i in ["Third", "Final"]:
        new_story_second_half = {
            "role": "user", "content": f"Write the {i} part of the story among 5 continuing from the previous part"+"in the "+direction+". Include a bold heading above the top starting with '{i} part:'. Limit your answer to 4 sentences or less"}
        messages.append(new_story_second_half)
        story = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages)
        system_message = story["choices"][0]["message"]
        messages.append(system_message)

    story_parts = []
    for message in messages:
        if message['role'] == 'assistant':
            story_parts.append(message['content'])

    illustration_parts = []

    for story_part in story_parts:
        illustration = openai.Image.create(
            prompt=story_part,
            n=1,
            size="256x256")
        image_url = illustration['data'][0]['url']
        illustration_parts.append(image_url)

    for i in range(len(story_parts)):
        story_parts[i] = story_parts[i].replace(". ", ".\n\n")

    return (story_parts[0], illustration_parts[0], story_parts[1], illustration_parts[1], story_parts[2], illustration_parts[2], story_parts[3], illustration_parts[3])


# EXAMPLE

key1 = "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"
name1 = "Jimmy"
situation1 = "broke college student recently graduated from HKU with no job. His girlfriend dumped him and parents disowned him. Living on the streets and see no hope for future"
direction1 = "gain motivation from unexpected kindness of people in society around him and eventually find a path to pursue his dream"

# INTERFACE

with gr.Blocks(title="StoryGPT", css="#button{background-color:#4CAF50} #title{text-align: center} footer{visibility: hidden}") as interface:

    gr.Markdown(
        """
    <img src="https://lean.social/wp-content/uploads/2023/02/logo_notext-1.svg"
     alt="Markdown Monster icon"
     style="margin-left:auto; margin-right:auto;margin-top:20px; max-width: 100px; padding-bottom:0px; margin-bottom:-50px" />,
     """, elem_id="image")

    gr.Markdown(
        """
    <h1 style="margin-bottom:0px">💁‍♀️ StoryGPT by LEAN Social 😿</h1>
    <h5 style="font-weight:normal; margin-top:0px">Visit <a href="https://lean.social">www.lean.social</a> to learn how we help young people study<h/5>
    <h4 style="margin-bottom:-30px; font-weight: normal"> Are you a student struggling with <strong><mark style="background-color:white; color:black">&nbsp peer, family, and society pressure? &nbsp</mark></strong></h3>
    <h4 style="font-weight: normal"> Paste in your life's struggles to see how it can be improved!</h3>
    """, elem_id="title")

    with gr.Row(elem_id="main"):

        with gr.Column(scale=1):
            gr.Markdown(
                """
                <h3>Start Here</h3>
                To find your OPEN API key, login to your OPENAI account and go <a href="https://platform.openai.com/account/api-keys">here</a>.<br><br>
                You can also click the example below to use my key for trial. <br><br>
                Only 1 story per user can be generated in 1 minute. Please use your API key if you can.
                """
            )
            key = gr.Textbox(label="Your OPENAI api key")
            name = gr.Textbox(label="Character's name")
            situation = gr.Textbox(
                label="What is the character's life situation?")
            direction = gr.Textbox(
                label="What direction do you want the story to go?")
            Generate_btn = gr.Button(value="Generate", elem_id="button")
            examples = gr.Examples(examples=[[key1, name1, situation1, direction1]], inputs=[
                key, name, situation, direction], label="Click here to test with our example")

        with gr.Column(scale=7, container=False):

            with gr.Row(variant="compact").style(equal_height=True):
                with gr.Column(scale=3):
                    story1 = gr.Textbox(show_label=False, lines=9).style(
                        container=False)

                with gr.Column(scale=1):
                    illustration1 = gr.Image(
                        show_label=False, brush_radius=0).style(height=200)

            with gr.Row(variant="compact").style(equal_height=True):
                with gr.Column(scale=3):
                    story2 = gr.Textbox(show_label=False, lines=9).style(
                        container=False)

                with gr.Column(scale=1):
                    illustration2 = gr.Image(
                        show_label=False, brush_radius=0, lines=9).style(height=200)

            with gr.Row(variant="compact").style(equal_height=True):
                with gr.Column(scale=3):
                    story3 = gr.Textbox(show_label=False, lines=9).style(
                        container=False)

                with gr.Column(scale=1):
                    illustration3 = gr.Image(
                        show_label=False, brush_radius=0).style(height=200)

            with gr.Row(variant="compact").style(equal_height=True):
                with gr.Column(scale=3):
                    story4 = gr.Textbox(show_label=False, lines=9).style(
                        container=False)

                with gr.Column(scale=1):
                    illustration4 = gr.Image(
                        show_label=False, brush_radius=0).style(height=200)

    inputs = [key, name, situation, direction]
    outputs = [story1, illustration1, story2,
               illustration2, story3, illustration3, story4, illustration4]

    Generate_btn.click(storyGPT, inputs=inputs, outputs=outputs)


interface.launch(favicon_path="Logo round bg.png")
