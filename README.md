# can-beeware-for-android-bridge-to-java

This repo is the ongoing attempt to connect beeware (https://beeware.org/) to Java using Chaquopy  https://chaquo.com/chaquopy/

As a simple example it follows the beeware Android tutorial to create a Toga form with a button.

👉 this is not working code yet, but instead a basis for discussion👈

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

