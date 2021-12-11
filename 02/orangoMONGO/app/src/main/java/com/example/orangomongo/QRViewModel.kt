package com.example.orangomongo

//import org.litote.kmongo.*
import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.android.volley.Request
import com.android.volley.toolbox.StringRequest
import java.text.ParseException
import java.text.SimpleDateFormat
import java.util.*

val middlewareURL = "http://192.168.20.64:80/valid/"

class QRViewModel(): ViewModel() {
    var personID: String = ""
    private lateinit var document: String
    var loading: Boolean = true
    var valid: Boolean = false
    var result: String = ""
    var color: String = "#FF0000"

    fun setID(data:String){
        personID = data
    }

    fun fetchDocument(
        instance: NetworkOp,
        onComplete: () -> Unit
    ){

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
                {
                    response -> Log.d("NETWORK", "error: $response")
                    valid = false
                    update()
                    onComplete()
                })
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
            result = "Sorry, your covid certificate isn't valid :("
            color = "#E06666"
        }
    }
}

// yeah, this is over the top. android development scares me because i don't understand it
// fully. so yes, i will gladly get me a factory.
// removed repository so this is useless now. oh well
class QRViewModelFactory() : ViewModelProvider.Factory {
    override fun <T : ViewModel?> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(QRViewModel::class.java)){
            @Suppress("UNCHECKED_CAST")
            return QRViewModel() as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}