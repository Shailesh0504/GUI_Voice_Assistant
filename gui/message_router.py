# gui/message_router.py

app_instance = None

def set_gui_instance(instance):
    global app_instance
    app_instance = instance

def show_in_chat(text):
    if app_instance:
        app_instance.append_message("🤖 Assistant", text)
