# Internship Curriculum: Heart Sound AI Classification

**Target:** Build a heart sound AI classifier (normal/abnormal + murmur detection) and deploy to Syntiant NDP200 edge NPU

**Duration:** 2 months (8 weeks)

**Prerequisites:** High school graduate, basic Python, curiosity to learn, Google account (for Colab + Drive)

---

## Month 1: Foundation & Baseline Binary Classifier

### Week 1 — Python & Google Colab Crash Course
| Day | Task |
|-----|------|
| 1-2 | Python refresher: numpy, pandas, matplotlib basics on [Google Colab](https://colab.research.google.com/) — run each concept in a Colab cell |
| 3-4 | ML basics: what is classification, training vs inference, overfitting, train/test split. Watch [3Blue1Brown neural network series](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) + [fast.ai lesson 1]((https://course.fast.ai/Lessons/lesson1.html)) |
| 5 | Set up Colab environment: connect Google Drive, mount it in Colab, verify you can run a PyTorch cell with GPU enabled (Runtime → Change runtime type → T4 GPU). Save your first Colab notebook |

**Week 1 Deliverable:** A Colab notebook with numpy/pandas/matplotlib basics + a working PyTorch cell on GPU. A 1-page summary of "how a neural network classifies heart sounds" in your own words.

### Week 2 — Heart Sound Fundamentals & Dataset Exploration (on Colab)
| Day | Task |
|-----|------|
| 1-2 | Read about heart sounds: S1, S2, systole, diastole, murmurs. Watch 2-3 cardiology YouTube videos on auscultation |
| 3-4 | Upload PhysioNet 2016 dataset to Google Drive. In Colab, mount Drive and write a notebook to: count files per class, plot recording duration distribution, listen to 5 normal + 5 abnormal samples |
| 5 | Use librosa to extract and visualize: waveform, spectrogram, MFCCs for one normal and one abnormal sample. Save comparison plots |

**Week 2 Deliverable:** A Colab notebook that loads PhysioNet 2016 from Google Drive, prints dataset stats, and displays waveform + spectrogram for 2 samples.

### Week 3 — Build Baseline CNN Classifier (on Colab GPU)
| Day | Task |
|-----|------|
| 1-2 | Implement audio preprocessing pipeline in Colab: resample to 2kHz, pad/truncate to 5s, compute mel-spectrogram (64 mel bands, hop length 512) |
| 3-4 | Build a simple CNN in PyTorch with `device = "cuda"`: Conv2D → ReLU → MaxPool → Conv2D → ReLU → MaxPool → FC → Softmax (2 classes). Train on 80/20 split using T4 GPU |
| 5 | Evaluate: plot confusion matrix, compute accuracy/sensitivity/specificity. Download/save the model checkpoint to Google Drive |

**Week 3 Deliverable:** A Colab notebook with full training pipeline + evaluation showing >= 75% accuracy. Model checkpoint saved in Google Drive.

### Week 4 — Improve & Analyze (on Colab)
| Day | Task |
|-----|------|
| 1-2 | Add data augmentation: time-stretch, pitch-shift, add noise. Re-train on Colab GPU, compare metrics |
| 3-4 | Experiment with architecture: add batch norm, dropout, try 3-4 conv layers. Log all experiments in a simple table inside the Colab notebook |
| 5 | Write a short report in the notebook: what worked, what didn't, final accuracy (target >85%), limitations |

**Week 4 Deliverable:** Final Colab notebook with >85% accuracy model + experiment log table + report. Model saved to Google Drive.

---

## Month 2: Multi-Class Classification & Edge Deployment

### Week 5 — CirCor DigiScope 2022 Multi-Class Dataset (on Colab)
| Day | Task |
|-----|------|
| 1-2 | Upload CirCor DigiScope 2022 dataset to Google Drive. From Colab, explore class distribution, recording lengths |
| 3 | Adapt preprocessing pipeline for CirCor in Colab: handle different sample rates, extract patient metadata |
| 4-5 | Modify baseline CNN for 3-class output. Train on Colab GPU, evaluate per-class metrics |

**Week 5 Deliverable:** Colab notebook exploring CirCor + 3-class classifier with per-class metrics. Model saved to Google Drive.

### Week 6 — Advanced Architecture & Comparison (on Colab)
| Day | Task |
|-----|------|
| 1-2 | Research and implement one advanced architecture from literature: either CNN+CBAM attention or CRNN (Conv + GRU) |
| 3-4 | Train the advanced model on Colab GPU, compare with baseline on both PhysioNet and CirCor |
| 5 | Select the best model, export to ONNX format from Colab, download to local machine |

**Week 6 Deliverable:** Colab notebook with both models compared in a table. Best model exported as `.onnx` file saved to Google Drive.

### Week 7 — Edge Impulse & Syntiant NDP200 Deployment
| Day | Task |
|-----|------|
| 1-2 | Sign up for Edge Impulse. Follow their "audio classification" tutorial to understand the platform workflow |
| 3 | Download the ONNX model from Google Drive. Import it into Edge Impulse (they support ONNX import) |
| 4-5 | Configure Syntiant NDP200 target in Edge Impulse. Build and download the deployment package |

**Week 7 Deliverable:** A deployed model binary targeting Syntiant NDP200. Screenshot of Edge Impulse dashboard showing successful build.

### Week 8 — Integration & Final Report
| Day | Task |
|-----|------|
| 1-2 | Write a script that: loads a heart sound → runs preprocessing → runs model inference → prints prediction. Test on 20 unseen samples |
| 3-4 | Document the full pipeline: dataset → preprocessing → training → export → edge deployment. Include diagrams |
| 5 | Prepare final presentation (5-10 slides): problem, dataset, architecture, results, edge deployment demo, lessons learned |

**Week 8 Deliverable:** Final report, GitHub repo with all code, demo script, and presentation.

---

## Weekly Milestone Summary

| Week | Milestone |
|------|-----------|
| 1 | Python/ML environment ready, basic NN understanding |
| 2 | PhysioNet 2016 explored, audio visualization working |
| 3 | Baseline CNN trained, >75% accuracy |
| 4 | Improved model >85% accuracy, experiment log |
| 5 | CirCor dataset explored, 3-class classifier working |
| 6 | Advanced model implemented, model comparison done |
| 7 | Edge Impulse deployment to Syntiant NDP200 |
| 8 | Demo script + final report + presentation |

## Success Criteria
- [ ] Baseline binary classifier >85% accuracy on PhysioNet 2016
- [ ] Multi-class classifier (3-class) on CirCor DigiScope
- [ ] Model exported and deployed to Syntiant NDP200 via Edge Impulse
- [ ] Final presentation delivered with live or recorded demo
