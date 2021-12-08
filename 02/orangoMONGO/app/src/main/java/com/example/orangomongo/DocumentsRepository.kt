package com.example.orangomongo

import android.util.Log
import io.realm.Realm
import io.realm.RealmObject
import io.realm.annotations.PrimaryKey
import io.realm.mongodb.App
import io.realm.mongodb.AppConfiguration
import io.realm.mongodb.Credentials
import io.realm.mongodb.User
import io.realm.mongodb.sync.SyncConfiguration
import org.bson.types.ObjectId
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors
import java.util.concurrent.FutureTask

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

class DocumentsRepository {
    // i think it's nicer to keep it in a repository, this way it's separated from app logic
    // could also be in ViewModel... i don't know enough.
    private val appID : String = "mongodb://sambud:sambud@realm.mongodb.com:27020/?authMechanism=PLAIN&authSource=%24external&ssl=true&appName=myapp-zcwdx:mongodb-atlas:local-userpass"
    val app = App(
            AppConfiguration.Builder(appID)
            .build())
    private val credentials: Credentials = Credentials.anonymous()

    fun login(onLoginFailed: (String)->Unit, onLoginSuccess: ()->Unit) {
        app.loginAsync(credentials){
            if (!it.isSuccess){
                onLoginFailed(it.error.message ?: "Login impossible, an error occured")
            } else onLoginSuccess()
        }
    }

}
