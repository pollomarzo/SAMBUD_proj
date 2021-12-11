package com.example.orangomongo

import android.graphics.Color
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.animation.Animation
import android.view.animation.AnimationUtils.loadAnimation
import androidx.fragment.app.activityViewModels
import androidx.navigation.fragment.findNavController
import com.example.orangomongo.databinding.FragmentResultBinding
import android.view.animation.AnimationUtils
import android.widget.ImageView

/**
 * A simple [Fragment] subclass as the second destination in the navigation.
 */
class ResultFragment : Fragment() {

    private var _binding: FragmentResultBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!
    private val model: QRViewModel by activityViewModels {
        QRViewModelFactory()
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
        binding.result.setTextColor(Color.parseColor(model.color))
        binding.result.text = model.result
        binding.personCode.text = model.personID
        binding.checkMark.visibility = if (model.valid) View.GONE else View.VISIBLE
        binding.checkMark2.visibility = if (model.valid) View.VISIBLE else View.GONE
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}