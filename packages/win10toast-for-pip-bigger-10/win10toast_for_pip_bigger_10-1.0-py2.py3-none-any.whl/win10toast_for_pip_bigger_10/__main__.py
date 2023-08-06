﻿from win10toast_for_pip_bigger_10 import ToastNotifier
import time

# #############################################################################
# ###### Stand alone program ########
# ###################################
if __name__ == "__main__":
    # Example
    toaster = ToastNotifier()
    toaster.show_toast(
        "Hello World!!!",
        "Python is 10 seconds awsm!",
        duration=10)
    toaster.show_toast(
        "Example two",
        "This notification is in it's own thread!",
        icon_path=None,
        duration=5,
        threaded=True
        )
    # Wait for threaded notification to finish
    while toaster.notification_active(): time.sleep(0.1)
