
import time
import threading
import cv2
import mss
import numpy as np
import pygame
from pynput import keyboard

CAPTURE_INTERVAL = 0.2
CHANGE_THRESHOLD = 1.5
PIXEL_SENSITIVITY = 35
ALARM_FILE = "alarm.wav"

alarm_active = False
monitoring_enabled = True

stop_requested = threading.Event()
enable_requested = threading.Event()
disable_requested = threading.Event()


def initialize_alarm():
    pygame.mixer.init()
    return pygame.mixer.Sound(ALARM_FILE)


def trigger_alarm(alarm_sound):
    global alarm_active

    if not alarm_active:
        print("\n!!! ALARM ACTIVATED !!!")
        alarm_sound.play(loops=-1)
        alarm_active = True


def stop_alarm(alarm_sound):
    global alarm_active

    if alarm_active:
        alarm_sound.stop()
        alarm_active = False
        print("\n[ALARM SILENCED]")


def on_key_press(key):
    if key == keyboard.Key.space:
        stop_requested.set()

    elif key == keyboard.Key.f8:
        enable_requested.set()

    elif key == keyboard.Key.f9:
        disable_requested.set()


def capture_screen(screen_capture):
    screenshot = screen_capture.grab(screen_capture.monitors[1])
    image = np.array(screenshot)
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    return grayscale_image


def compare_frames(previous_frame, current_frame):
    difference = cv2.absdiff(previous_frame, current_frame)

    _, threshold_image = cv2.threshold(
        difference,
        PIXEL_SENSITIVITY,
        255,
        cv2.THRESH_BINARY
    )

    changed_pixels = np.count_nonzero(threshold_image)
    total_pixels = threshold_image.size

    change_percentage = (changed_pixels / total_pixels) * 100

    return change_percentage


def main():
    global monitoring_enabled

    alarm_sound = initialize_alarm()

    listener = keyboard.Listener(on_press=on_key_press)
    listener.start()

    print("Monitoring started.")
    print("F8 = Enable monitoring")
    print("F9 = Disable monitoring")
    print("SPACE = Silence alarm")
    print("CTRL+C = Exit\n")

    try:
        with mss.mss() as screen_capture:
            previous_frame = capture_screen(screen_capture)

            while True:
                time.sleep(CAPTURE_INTERVAL)

                if enable_requested.is_set():
                    enable_requested.clear()

                    if not monitoring_enabled:
                        monitoring_enabled = True
                        previous_frame = capture_screen(screen_capture)
                        print("\n[MONITORING ENABLED]")

                if disable_requested.is_set():
                    disable_requested.clear()

                    if monitoring_enabled:
                        monitoring_enabled = False
                        stop_alarm(alarm_sound)
                        print("\n[MONITORING DISABLED]")

                if stop_requested.is_set():
                    stop_requested.clear()
                    stop_alarm(alarm_sound)

                current_frame = capture_screen(screen_capture)

                if monitoring_enabled:
                    change_percentage = compare_frames(
                        previous_frame,
                        current_frame
                    )

                    if change_percentage >= CHANGE_THRESHOLD:
                        print(
                            f"[MOTION DETECTED] "
                            f"Change: {change_percentage:.2f}%"
                        )
                        trigger_alarm(alarm_sound)

                    else:
                        print(
                            f"[MONITORING] "
                            f"Change: {change_percentage:.2f}%"
                        )

                previous_frame = current_frame

    finally:
        listener.stop()
        alarm_sound.stop()
        pygame.mixer.quit()


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

    except Exception as error:
        print(f"\nUnexpected error: {error}")
