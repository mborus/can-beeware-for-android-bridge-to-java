# can-beeware-for-android-bridge-to-java

This repo is the ongoing attempt to connect beeware (https://beeware.org/) to Java using Chaquopy  https://chaquo.com/chaquopy/

As a simple example it follows the beeware Android tutorial to create a Toga form with a button.

👉 this example now works from Windows 11 to a Android 11 device 👈

The simple java class is

```

package org.beeware.android;

/**
 * A simple Java counter class. Each time the value is read via {@link #read()},
 * it returns the current value, then increments the counter by one.
 */
public class AutoCounter {
    private int value = 0;

    public AutoCounter() {
    }

    /**
     * Return the current counter value, then increment it.
     *
     * @return the value before incrementing
     */
    public int read() {
        return value++;
    }
}

```

The aim of the code is to put a button on a Toga form that uses this counter class.
The code only needs to run on a connected hardware Android device. I'm testing with Android 11 and 15.

~~The java example is in the folder `java_src` - it is not in the correct place and it includes a compiled jar file that should not be needed.~~
The java code is in `androidjavaexperiment/android/java/org/beeware/android/AutoCounter.java`.
The folder `java_src` is no longer in use.

The easiest way to get started is to follow the beeware tutorial (https://docs.beeware.org/en/latest/tutorial/tutorial-0.html) until step 5 (Android) and then 
modify the project to match this repo.

The changes are in file `androidjavaexperiment/src/androidjavaexperiment/app.py`. 



The pyproject.toml file has been extended to include out own AutoCounter.java file.

```
build_gradle_extra_content = """
android.sourceSets.main.java.srcDirs += '../../../../../android/java'
"""
```

Installation:
##############

- Python 3.13.7, venv
- install beeware, briefcase, toga
- briefcase new

from the command line:

briefcase create  android -v
briefcase build  android -v
briefcase run  android -v

Note: After every change to the pyproject.toml file, I'm currently deleting the build folder and rebuild.
