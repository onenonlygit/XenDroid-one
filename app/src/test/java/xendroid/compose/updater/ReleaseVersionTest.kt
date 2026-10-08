package xendroid.compose.updater

import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class ReleaseVersionTest {
    @Test fun onlyNewerForkReleaseIsOffered() {
        assertTrue(isNewerRelease("<!-- xendroid-one-version-code:1002 -->", 1001))
        assertFalse(isNewerRelease("<!-- xendroid-one-version-code:1001 -->", 1001))
        assertFalse(isNewerRelease("<!-- xendroid-one-version-code:1000 -->", 1001))
    }

    @Test fun missingOrInvalidCodeDoesNotOfferUntrustedRelease() {
        assertFalse(isNewerRelease(null, 1001))
        assertFalse(isNewerRelease("Original XenDroid release", 1001))
        assertFalse(isNewerRelease("<!-- xendroid-one-version-code:999999999999 -->", 1001))
    }
}
