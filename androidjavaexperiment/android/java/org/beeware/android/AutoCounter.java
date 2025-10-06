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
