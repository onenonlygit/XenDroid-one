package xendroid.compose.updater

/** A release without the fork's explicit Android versionCode is not an update. */
internal fun isNewerRelease(body: String?, installedCode: Int): Boolean {
    val code = Regex("<!--\\s*xendroid-one-version-code:(\\d+)\\s*-->")
        .find(body.orEmpty())?.groupValues?.get(1)?.toIntOrNull() ?: return false
    return code > installedCode
}
