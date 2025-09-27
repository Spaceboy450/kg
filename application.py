import gradio as gr
from src.image_processing import filter_and_sort_zip


def wrapper_filter_and_sort_zip(zip_file, color, tolerance, rows, cols, orientation):
    try:
        all_images, left_images, right_images, pdf_path, pdf_preview_html, error_msg = filter_and_sort_zip(
            zip_file, color, tolerance, rows, cols, orientation
        )

        if not error_msg or error_msg.strip() == "":
            error_msg = "Ошибок нет! Программа отработала успешно!"

        return all_images, left_images, right_images, pdf_path, pdf_preview_html, error_msg

    except Exception as e:
        return [], [], [], None, "", f"Ошибка при обработке: {str(e)}"


with gr.Blocks() as demo:
    gr.Markdown("## Фильтр изображений по цвету (ZIP) + PDF")

    with gr.Row():
        upload = gr.File(label="Загрузить ZIP", file_types=[".zip"], type="file")

    color = gr.ColorPicker(value="#ff0000", label="Цвет")
    tolerance = gr.Slider(0, 100, value=10, label="Допуск (%)")

    with gr.Row():
        rows = gr.Slider(1, 5, value=5, step=1, label="Количество строк")
        cols = gr.Slider(1, 5, value=5, step=1, label="Количество колонок")
        orientation = gr.Radio(
            ["portrait", "landscape"],
            value="portrait",
            label="Ориентация страницы",
        )

    filter_btn = gr.Button("Отобрать")

    with gr.Tabs():
        with gr.TabItem("Все подходящие"):
            all_images = gr.Gallery(label="Все изображения", show_label=True, columns=4)
        with gr.TabItem("Против часовой"):
            left_images = gr.Gallery(label="Левая колонка", show_label=True, columns=4)
        with gr.TabItem("По часовой"):
            right_images = gr.Gallery(label="Правая колонка", show_label=True, columns=4)

    with gr.Row():
        pdf_download = gr.File(label="Скачать PDF", interactive=False)

    pdf_preview = gr.HTML(label="Предпросмотр PDF")
    error_box = gr.Textbox(label="Ошибки обработки", interactive=False, lines=10)

    filter_btn.click(
        wrapper_filter_and_sort_zip,
        [upload, color, tolerance, rows, cols, orientation],
        [all_images, left_images, right_images, pdf_download, pdf_preview, error_box],
    )


if __name__ == "__main__":
    demo.launch()