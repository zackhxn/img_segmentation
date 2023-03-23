import os
import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog
import gradio as gr
from scripts.openpose.util import img_segmentation
import modules.scripts as scripts
from modules import script_callbacks
from PIL import Image

body_estimation = None
maps_path = os.path.join(scripts.basedir(), "maps");
types = list(os.walk(maps_path))[0][1]
class Script(scripts.Script):
  def __init__(self) -> None:
    super().__init__()

  def title(self):
    return "Image Editor"

  def show(self, is_img2img):
    return scripts.AlwaysVisible

  def ui(self, is_img2img):
    return ()


def call_img_segmentation():
   # 弹出文件对话框，让用户选择一张图片
   root = tk.Tk()
   # root.withdraw()
   # root.mainloop()
   file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
   root.quit()
   # print("Selected file:", file_path)
   img_segmentation(file_path)




def on_ui_tabs():
  png_input_area = gr.Image(label="Selected")
  with gr.Blocks(analytics_enabled=False) as openpose_editor:
    with gr.Row():
      with gr.Column():
        width = gr.Slider(label="width", minimum=64, maximum=2048, value=512, step=64, interactive=True)
        height = gr.Slider(label="height", minimum=64, maximum=2048, value=512, step=64, interactive=True)
        with gr.Row():
          add = gr.Button(value="Add Pose", variant="primary")
          # img = gr.Button(value="edit img", variant="primary")
          # delete = gr.Button(value="Delete")
        with gr.Row():
          reset_btn = gr.Button(value="Reset")
          json_input = gr.Button(value="Load from JSON")
          # png_input = gr.Button(value="Detect from image")
          # png_input_area = gr.Image(label="Detect from image", elem_id="openpose_editor_input")
          # bg_input = gr.Button(value="Add image")
          png_input = gr.UploadButton(label="Add image", file_types=["image"], type="bytes",
                                      elem_id="openpose_detect_button")
        with gr.Row():
          with gr.Column(scale=3):
            for t in types:
              with gr.Tab(t.capitalize()):
                dataset = gr.Examples(examples=os.path.join(maps_path, t), inputs=[png_input_area],examples_per_page=24,label="Depth Maps", elem_id="examples")
          with gr.Column(scale=1):
            png_input_area.render()



            opacity = gr.Slider(label="Opacity", minimum=0.01, maximum=1, value=1, step=0.01, interactive=True)
            with gr.Row():
              segmentation = gr.Button(value="Img Segmentation" ,variant="primary")
              add_select = gr.Button(value="Add", variant="primary")


      with gr.Column():
        # gradioooooo...
        canvas = gr.HTML('<canvas id="openpose_editor_canvas" width="512" height="512" style="margin: 0.25rem; border-radius: 0.25rem; border: 0.5px solid"></canvas>')
        jsonbox = gr.Text(label="json", elem_id="hide_json")
        with gr.Row():
          # json_output = gr.Button(value="Save JSON")
          png_output = gr.Button(value="Save PNG")
          pose_output = gr.Button(value="Save Openpose")
          send_t2t = gr.Button(value="Send to txt2img")
          send_i2i = gr.Button(value="Send to img2img")
          select_target_index = gr.Dropdown([str(i) for i in range(10)], label="Send to", value="0", interactive=True)

    # def estimate(img):
    #   global body_estimation
    #
    #   if body_estimation is None:
    #     if not os.path.isfile((os.path.join(scripts.basedir(), "models/body_pose_model.pth"))):
    #       body_model_path = "https://huggingface.co/lllyasviel/ControlNet/resolve/main/annotator/ckpts/body_pose_model.pth"
    #       load_file_from_url(body_model_path, model_dir=os.path.join(scripts.basedir(), "models"))
    #     body_estimation = Body('models/body_pose_model.pth')
    #
    #   candidate, subset = body_estimation(pil2cv(img))
    #
    #   result = {
    #     "candidate": candidate2li(candidate),
    #     "subset": subset2li(subset)
    #   }
    #
    #   return result



    width.change(None, [width, height], None, _js="(w, h) => {resizeCanvas(w, h)}")
    height.change(None, [width, height], None, _js="(w, h) => {resizeCanvas(w, h)}")
    pose_output.click(None, [], None, _js="savePose")
    png_output.click(None, [], None, _js="savePNG")
    png_input.upload(None, png_input, [width, height], _js="addBackground")
    # png_input.click(None, [], None, _js="detectImage")
    add.click(None, [], None, _js="addPose")

    # img.click(select_image)

    # png_input_area.change(estimate, [png_input_area], [jsonbox])
    send_t2t.click(None, [], None, _js="() => {sendImage('txt2img')}")
    send_i2i.click(None, [], None, _js="() => {sendImage('img2img')}")
    select_target_index.change(None, [select_target_index], None, _js="(i) => {updateTargetIndex(parseInt(i, 10))}")
    reset_btn.click(None, [], None, _js="resetCanvas")
    json_input.click(None, None, [width, height], _js="loadJSON")
    # json_output.click(None, None, None, _js="saveJSON")
    add_select.click(None, [png_input_area], None, _js="(path) => {addImg(path)}")
    # add_select.click(call_img_segmentation, [png_input_area], None, _js="")
    # print("****",type(png_input_area))
    segmentation.click(call_img_segmentation,[],None,_js="")



  return [(openpose_editor, "Image Sagmentation", "openpose_editor")]

script_callbacks.on_ui_tabs(on_ui_tabs)
