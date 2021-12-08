package com.example.orangomongo

import android.app.Activity
import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import org.bson.codecs.pojo.annotations.BsonId
//import org.litote.kmongo.*
import io.realm.Realm
import io.realm.RealmObject
import io.realm.annotations.PrimaryKey
import io.realm.kotlin.where
import io.realm.mongodb.sync.SyncConfiguration
import org.bson.types.ObjectId



class QRViewModel(private val repository: DocumentsRepository): ViewModel() {
    var personID: String = ""
    private lateinit var document: String
    var loading: Boolean = true
    var valid: Boolean = false
    private lateinit var realm: Realm

    fun setID(data:String){
        personID = data
    }

    fun fetchDocument(){
        //val client = KMongo.createClient("mongodb+srv://mamoud:mamoud1@smbud-2.2dbjr.mongodb.net/test")
        //val database = client.getDatabase("mamoud")
        //val col = database.getCollection<DBDocument>("people100")
        //Log.d("DB", "got collection, try to find item 1: " +
        //        col.findOne(DBDocument::First_Name eq "Henry").toString())
        Log.d("DB", "fetching...")
        val user = repository.app.currentUser()
        Log.d("DB", "built config object")
        val config = SyncConfiguration.Builder(user!!, "user=$(user!!.id)")
            .build()
        Realm.getInstanceAsync(config, object:Realm.Callback(){
            override fun onSuccess(realm: Realm) {
                // save realm so we can close it at the end (could close it right away but
                // this way changes are easier)
                this@QRViewModel.realm = realm
                loading = false
                valid = isValid(realm)
                Log.d("DB", "correctly obtained realm")
            }
        })
    }
    private fun isValid(realm:Realm): Boolean{
        val doc: DBDocument? = realm.where<DBDocument>().equalTo("_id", personID).findFirst()
        Log.d("DB", "holy shit it works! result: $doc")
        //val version = doc?.Validity?.get(0)?.Version
        //val expirationDate = doc?.Validity?.get(0)?.Expiration_Date
        if(doc?.First_Name != "giorgio")
            return true
        return false
    }

    override fun onCleared() {
        super.onCleared()
        repository.app.currentUser().run { realm.close() }
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