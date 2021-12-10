package com.example.orangomongo

import android.content.Intent
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.activityViewModels
import androidx.navigation.fragment.findNavController
import com.example.orangomongo.databinding.FragmentScanBinding
import com.google.zxing.integration.android.IntentIntegrator

/**
 * A simple [Fragment] subclass as the default destination in the navigation.
 */
class ScanFragment : Fragment() {

    private var _binding: FragmentScanBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!
    private val model: QRViewModel by activityViewModels {
        QRViewModelFactory((activity?.application as DocumentsApplication).repository)
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        Log.d("CAMERA", "onCreateView called")
        _binding = FragmentScanBinding.inflate(inflater, container, false)
        return binding.root

    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        binding.buttonFirst.setOnClickListener {
            binding.buttonFirst.isEnabled = false
            val intentIntegrator = IntentIntegrator(activity)
            intentIntegrator.setBeepEnabled(false)
            intentIntegrator.setCameraId(0)
            intentIntegrator.setPrompt("SCAN")
            intentIntegrator.setBarcodeImageEnabled(false)
            intentIntegrator.initiateScan()
            binding.loading.visibility = View.VISIBLE
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        Log.d("SCANFRAGMENT", "activityResult received")
        val cameraResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, data)
        Log.d("CAMERA", "SCANNED")
        if (cameraResult != null){
            if (cameraResult.contents == null) {
                Toast.makeText(
                    activity,
                    "cancelled",
                    Toast.LENGTH_SHORT).show()
            } else {
                Log.d("CAMERA", "SCANNED CORRECTLY")
                val code = cameraResult.contents
                model.setID(code)
                Toast.makeText(activity,
                    "Scanned correctly! Result: $code",
                    Toast.LENGTH_SHORT)
                    .show()
                if(activity?.applicationContext != null) model.fetchDocument(NetworkOp.getInstance(
                    requireActivity().applicationContext)
                ) {
                    findNavController().navigate(R.id.action_ScanFragment_to_ResultFragment)
                    binding.loading.visibility = View.GONE
                    binding.buttonFirst.isEnabled = true}
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}