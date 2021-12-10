package com.example.orangomongo

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.activityViewModels
import androidx.navigation.fragment.findNavController
import com.example.orangomongo.databinding.FragmentResultBinding

/**
 * A simple [Fragment] subclass as the second destination in the navigation.
 */
class ResultFragment : Fragment() {

    private var _binding: FragmentResultBinding? = null

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

        _binding = FragmentResultBinding.inflate(inflater, container, false)
        return binding.root

    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        binding.result.text = if(model.valid)
            "Nice! Your covid certification works!"
        else "Sorry, your covid thingy isn't valid :("
        binding.personCode.text = model.personID
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}