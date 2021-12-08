package com.example.orangomongo

import android.content.Intent
import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.navigateUp
import androidx.navigation.ui.setupActionBarWithNavController
import android.view.Menu
import android.view.MenuItem
import androidx.activity.viewModels
import com.example.orangomongo.databinding.ActivityMainBinding
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.google.zxing.integration.android.IntentIntegrator


class MainActivity : AppCompatActivity() {

    private lateinit var appBarConfiguration: AppBarConfiguration
    private lateinit var binding: ActivityMainBinding
    private val model: QRViewModel by viewModels{
        QRViewModelFactory((this.application as DocumentsApplication).repository)
    }


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setSupportActionBar(binding.toolbar)

        val navController = findNavController(R.id.nav_host_fragment_content_main)
        appBarConfiguration = AppBarConfiguration(navController.graph)
        setupActionBarWithNavController(navController, appBarConfiguration)
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        // Inflate the menu; this adds items to the action bar if it is present.
        menuInflater.inflate(R.menu.menu_main, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        return when (item.itemId) {
            R.id.action_settings -> true
            else -> super.onOptionsItemSelected(item)
        }
    }
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        Log.d("CAMERA", "mainActivity onActivityResult called")
        val cameraResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, data)
        Log.d("CAMERA", "SCANNED")
        if (cameraResult != null){
            if (cameraResult.contents == null) {
                Toast.makeText(
                    this,
                    "cancelled",
                    Toast.LENGTH_SHORT).show()
            } else {
                Log.d("CAMERA", "SCANNED CORRECTLY")
                val code = cameraResult.contents
                model.setID(code)
                Toast.makeText(this,
                    "Scanned correctly! Result: $code",
                    Toast.LENGTH_SHORT)
                    .show()
                val fragment = supportFragmentManager.findFragmentById(R.id.ScanFragment)
                Log.d("FRAGMENT", fragment.toString())
                fragment?.onActivityResult(requestCode, resultCode, data)
            }
        }

        super.onActivityResult(requestCode, resultCode, data)

    }

    override fun onSupportNavigateUp(): Boolean {
        val navController = findNavController(R.id.nav_host_fragment_content_main)
        return navController.navigateUp(appBarConfiguration)
                || super.onSupportNavigateUp()
    }
}