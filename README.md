# can-beeware-for-android-bridge-to-java

This repo is the ongoing attempt to connect beeware (https://beeware.org/) to Java using Chaquopy  https://chaquo.com/chaquopy/

As a simple example it follows the beeware Android tutorial to create a Toga form with a button.

👉 this is not working code yet, but instead a basis for discussion 👈

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
The java example is in the folder `java_src` - it is not in the correct place and it includes a compiled jar file that should not be needed.

The easiest way to get started is to follow the beeware tutorial (https://docs.beeware.org/en/latest/tutorial/tutorial-0.html) until step 5 (Android) and then 
modify the project to match this repo.


Installation:
##############

- Python 3.13.7, venv
- install beeware, briefcase, toga
- briefcase new

from the command line:

briefcase create  android -v
briefcase build  android -v
briefcase run  android -v

The first run will give this error

org.beeware.android.MainActivity}: com.chaquo.python.PyException: java.lang.NoClassDefFoundError: org.beeware.android.AutoCounter

To fix this I create a `libs` folder in the build directory
(androidjavaexperiment/build/androidjavaexperiment/android/gradle/app/libs)

I manually create a jar file for AutoCounter.java using windows powershell

```
$src = "java_src"  # I added java_src/org/beeware/android/AutoCounter.java for convenience

if (Test-Path out) { Remove-Item -Recurse -Force out }; New-Item -ItemType Directory out | Out-Null

javac --release 8 -d out $(Get-ChildItem -Recurse -Filter *.java $src | ForEach-Object { $_.FullName })

ìf (Test-Path autocounter.jar) { Remove-Item autocounter.jar }

jar cf autocounter.jar -C out .
```

Copying 

androidjavaexperiment/build/androidjavaexperiment/android/gradle/app/libs/autocounter.jar

from 

androidjavaexperiment/java_src/org/beeware/android/autocounter.jar

After copying I run

briefcase update  android -v

briefcase build  android -v -u

briefcase run  android -v

Now the Toga form runs on the Andriod device.

The click to count button works and shows an alert with the counter.

👉 Aim of this project 👈 

Find out how to avoid having to create a jar file and manually copying it to a project

Side quest: Learn about jar vs aar files

