package com.example.orangomongo

import android.app.Application
import android.content.Context
import io.realm.Realm

class DocumentsApplication : Application() {
    val repository by lazy {
        DocumentsRepository()
    }

    override fun onCreate() {
        super.onCreate()
        Realm.init(this)
    }

}