package com.example.orangomongo

import android.app.Activity
import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.StringRequest
import org.bson.codecs.pojo.annotations.BsonId
//import org.litote.kmongo.*
import io.realm.Realm
import io.realm.RealmObject
import io.realm.annotations.PrimaryKey
import io.realm.kotlin.where
import io.realm.mongodb.sync.SyncConfiguration
import org.bson.types.ObjectId
import java.lang.NullPointerException
import java.text.ParseException
import java.text.SimpleDateFormat
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.util.*
import javax.security.auth.login.LoginException

val middlewareURL = "http://192.168.1.192:81/valid/"

class QRViewModel(private val repository: DocumentsRepository): ViewModel() {
    var personID: String = ""
    private lateinit var document: String
    var loading: Boolean = true
    var valid: Boolean = false
    var result: String = ""
    var color: String = "#FF0000"
    var check: Boolean = false



    /*fun login(onLoginError: (String)->Unit, onLoginSuccess: ()->Unit ){
        repository.login(
            onLoginError,
            onLoginSuccess)
    }
    */

    fun setID(data:String){
        personID = data
    }

    fun fetchDocument(
        instance: NetworkOp,
        onComplete: () -> Unit
    ){
        //val client = KMongo.createClient("mongodb+srv://mamoud:mamoud1@smbud-2.2dbjr.mongodb.net/test")
        //val database = client.getDatabase("mamoud")
        //val col = database.getCollection<DBDocument>("people100")
        //Log.d("DB", "got collection, try to find item 1: " +
        //        col.findOne(DBDocument::First_Name eq "Henry").toString())
        /*Log.d("DB", "fetching...")
        val user = repository.app.currentUser()
            //?: throw LoginException("Login wasn't completed correctly. User is null")

        val config = SyncConfiguration.Builder(user!!, "giorgio")
            .build()
        Log.d("DB", "built config object")

        Realm.getInstanceAsync(config, object:Realm.Callback(){
            override fun onSuccess(realm: Realm) {
                // save realm so we can close it at the end (could close it right away but
                // this way changes are easier)
                this@QRViewModel.realm = realm
                loading = false
                valid = isValid(realm)
                Log.d("DB", "correctly obtained realm")
            }
        })*/
        val reqURL = middlewareURL + personID
        Log.d("NETWORK", "requesting validity for id $personID, with url $reqURL")
        instance.addToRequestQueue(
            StringRequest(Request.Method.GET, reqURL,
                { response ->
                    Log.d("NETWORK", "received response: $response")
                    valid = isValid(response)
                    update()
                    Log.d("RESULT", "based on response $response, date is $valid")
                    onComplete()
                },
                { response -> Log.d("NETWORK", "error: $response") })
        )
    }
    private fun isValid(date:String): Boolean{
        var date_parsed: Date?
        try {
            date_parsed = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).parse(date)
        } catch (exc: ParseException) {
            return false
        }
        return date_parsed != null && Calendar.getInstance().time > date_parsed

    }
    private fun update(){
        if(valid){
            result="Nice! Your covid certification works!"
            color = "#00FF00"
        }
        else{
            result = "Sorry, your covid thingy isn't valid :("
            color = "#E06666"
        }
    }

    override fun onCleared() {
        super.onCleared()
        //repository.app.currentUser().run { realm.close() }
    }


}

// yeah, this is over the top. android development scares me because i don't understand it
// fully. so yes, i will gladly get me a factory.
class QRViewModelFactory(private val repository: DocumentsRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel?> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(QRViewModel::class.java)){
            @Suppress("UNCHECKED_CAST")
            return QRViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}