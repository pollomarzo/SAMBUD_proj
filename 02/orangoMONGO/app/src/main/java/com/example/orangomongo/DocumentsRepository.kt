package com.example.orangomongo

import android.util.Log
import io.realm.Realm
import io.realm.RealmObject
import io.realm.annotations.PrimaryKey
import io.realm.log.LogLevel
import io.realm.log.RealmLog
import io.realm.mongodb.App
import io.realm.mongodb.AppConfiguration
import io.realm.mongodb.Credentials
import io.realm.mongodb.User
import io.realm.mongodb.sync.SyncConfiguration
import org.bson.types.ObjectId
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors
import java.util.concurrent.FutureTask
import javax.security.auth.login.LoginException

data class DocValidity(
    val Version: String,
    val Expiration_Date: String,
)

open class DBDocument(
    @PrimaryKey
    var _id: ObjectId = ObjectId(),
    var First_Name: String? = null,
    var Last_Name: String? = null,
    //val Validity: Array<DocValidity>
): RealmObject()

// global Kotlin extension that resolves to the short version
// of the name of the current class. Used for labelling logs.
inline fun <reified T> T.TAG(): String = T::class.java.simpleName

class DocumentsRepository {
    /*// i think it's nicer to keep it in a repository, this way it's separated from app logic
    // could also be in ViewModel... i don't know enough.
    private val appID : String = "mongodb://sambud:sambud@realm.mongodb.com:27020/?" +
                "authMechanism=PLAIN&authSource=%24external&ssl=true&" +
                "appName=myapp-zcwdx:mongodb-atlas:local-userpass"
    var app: App = App(
        AppConfiguration.Builder(BuildConfig.MONGODB_REALM_APP_ID)
            .defaultSyncErrorHandler { session, error ->
                Log.e(TAG(), "Sync error: ${error.errorMessage}")
            }
            .build())

    // i'll keep it here since we don't need credentials. and if we do, always the same ones
    private val credentials: Credentials = Credentials.anonymous()

    init {
        RealmLog.setLevel(LogLevel.ALL)
    }

    fun login(onLoginFailed: (String)->Unit, onLoginSuccess: ()->Unit) {
        app.loginAsync(credentials){
            if (!it.isSuccess){
                Log.e("DB", "credentials: $credentials, ")
                throw LoginException(it.error.toString())
                onLoginFailed(it.error.message ?: "Login impossible, an error occured")
            } else {
                onLoginSuccess()
            }
        }
    }*/


}
