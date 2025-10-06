"""
Android Java Experiment using Beeware
"""

import toga
from toga.style.pack import COLUMN, ROW

def _make_counter():
    # Import Chaquopy bridge lazily to ensure Android classloader is ready.
    from java import jclass  # Chaquopy bridge
    AutoCounter = jclass("org.beeware.android.AutoCounter")
    return AutoCounter()

class AndroidJavaExperiment(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(style=toga.style.Pack(direction=COLUMN))

        button = toga.Button(
            "Click to count!",
            on_press=self.say_hello,
            margin=5,
        )
        main_box.add(button)

        # Add a label to display the last received broadcast
        self.broadcast_label = toga.Label(
            "Registering receiver...",
            margin=5,
        )
        main_box.add(self.broadcast_label)

        self.main_window = toga.MainWindow(title="version 0.0.1")
        self.main_window.content = main_box
        self.main_window.show()

        self.counter = _make_counter()
        
        # Setup broadcast receiver
        self.receiver_instance = None
        self.last_scan_data = None
        self.setup_and_register_receiver()

    def setup_and_register_receiver(self):
        """Setup and register the broadcast receiver with Android."""
        try:
            from java import dynamic_proxy, jarray, jbyte, jclass
            from android.content import IntentFilter
            from android.os import Handler, Looper
            
            # Store reference to the app instance for the callback
            app_instance = self
            
            # Create a handler for the main thread to update UI
            main_handler = Handler(Looper.getMainLooper())
            
            # Define the BroadcastReceiver using dynamic_proxy
            # dynamic_proxy doesn't require pre-compiled classes
            def onReceive(context, intent):
                print("onReceive called")
                if intent is None:
                    print("Intent is None")
                    return
                
                action = intent.getAction()
                print(f"Received intent with action: {action}")
                
                extras = intent.getExtras()
                if extras is None:
                    print("Extras is None")
                    return

                if extras.containsKey("EXTRA_EVENT_DECODE_VALUE"):
                    print("Found EXTRA_EVENT_DECODE_VALUE")
                    b = intent.getByteArrayExtra("EXTRA_EVENT_DECODE_VALUE")  # byte[]
                    
                    if b is not None:
                        # Convert Java byte[] -> Python bytes
                        app_instance.last_scan_data = bytes(jarray(jbyte)(b))
                        
                        # Update UI on main thread
                        def update_ui():
                            try:
                                decoded_value = app_instance.last_scan_data.decode('utf-8')
                                app_instance.broadcast_label.text = f"Received: {decoded_value}"
                                print(f"Broadcast received: {decoded_value}")
                            except Exception as e:
                                app_instance.broadcast_label.text = f"Received {len(app_instance.last_scan_data)} bytes"
                                print(f"Broadcast received ({len(app_instance.last_scan_data)} bytes): {e}")
                        
                        # Post to main thread
                        main_handler.post(dynamic_proxy('java.lang.Runnable', update_ui))
                    else:
                        print("Byte array is None")
                else:
                    print("EXTRA_EVENT_DECODE_VALUE not found in extras")
                    print(f"Available keys: {list(extras.keySet())}")
            
            # Create the receiver using dynamic_proxy
            self.receiver_instance = dynamic_proxy(
                'android.content.BroadcastReceiver',
                onReceive
            )
            
            # Get the Android activity context
            PythonActivity = jclass("org.beeware.android.MainActivity")
            activity = PythonActivity.singletonThis
            
            # Create an intent filter for the broadcast action
            intent_filter = IntentFilter("com.example.EVENT")
            
            # Register the receiver
            activity.registerReceiver(self.receiver_instance, intent_filter)
            
            print("Broadcast receiver registered successfully")
            self.broadcast_label.text = "Receiver registered, waiting for broadcasts..."
            
        except Exception as e:
            print(f"Error registering broadcast receiver: {e}")
            import traceback
            traceback.print_exc()
            self.broadcast_label.text = f"Error: {e}"

    async def say_hello(self, widget):
        # Read the current value from the Java counter, which auto-increments.
        value = self.counter.read()

        # Also show the last scan if available
        last_scan_info = ""
        if self.last_scan_data:
            try:
                decoded = self.last_scan_data.decode('utf-8')
                last_scan_info = f"\n\nLast scan: {decoded}"
            except:
                last_scan_info = f"\n\nLast scan: {len(self.last_scan_data)} bytes"

        await self.main_window.dialog(
            toga.InfoDialog(
                "Counter",
                f"I counted {value}!{last_scan_info}",
            )
        )

    def shutdown(self):
        """Unregister the broadcast receiver when the app closes."""
        try:
            if self.receiver_instance is not None:
                from java import jclass
                PythonActivity = jclass("org.beeware.android.MainActivity")
                activity = PythonActivity.singletonThis
                activity.unregisterReceiver(self.receiver_instance)
                print("Broadcast receiver unregistered")
        except Exception as e:
            print(f"Error unregistering broadcast receiver: {e}")
        
        return super().shutdown()

def main():
    return AndroidJavaExperiment()
