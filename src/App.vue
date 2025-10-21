<script setup>
import { ref, reactive } from 'vue';
import axios from 'axios';

const GRADES = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F"];
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL; 

const cgpaData = reactive({
  current_cgpa: 0.00,
  credits_taken: 0,
  subjects: [
    { credit: 0, old_grade: '', new_grade: '', grade:''}
  ]
});

const resultCgpa = ref(null);
const isLoading = ref(false);
const error = ref(null);

const addSubject = () => {
  cgpaData.subjects.push({ credit: 0, old_grade: '', new_grade: '' });
};

const removeSubject = (index) => {
  cgpaData.subjects.splice(index, 1);
};

const handleCalculation = async () => {
  resultCgpa.value = null;
  error.value = null;
  isLoading.value = true;
  try {
    const response = await axios.post(`${API_BASE_URL}/calculate-cgpa`, cgpaData);
    resultCgpa.value = response.data.new_cgpa;
  } catch (err) {
    error.value = `Backend error : ${err.response.status} ${err.response.statusText}`;
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="bg-slate-100 min-h-screen font-sans flex items-center justify-center p-4">
    <div class="w-full max-w-5xl bg-white rounded-2xl shadow-xl p-8 space-y-8">
      
      <header class="text-center">
        <h1 class="text-4xl font-bold text-slate-800">🎓 UM CGPA Recalculator</h1>
        <p class="text-slate-500 mt-2">Estimate your new CGPA after repeating subjects.</p>
      </header>

      <form @submit.prevent="handleCalculation">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label for="current-cgpa" class="block text-sm font-medium text-slate-600 mb-1">Current CGPA</label>
            <input type="number" id="current-cgpa" v-model.number="cgpaData.current_cgpa" min="0" max="4" step="0.01" class="placeholder:test w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"/>
          </div>
          <div>
            <label for="credits-taken" class="block text-sm font-medium text-slate-600 mb-1">Total Credits Taken</label>
            <input type="number" id="credits-taken" v-model.number="cgpaData.credits_taken" min="0" step="1" class="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"/>
          </div>
        </div>

        <hr class="my-8 border-slate-200" />

        <h2 class="text-2xl font-semibold text-slate-700 mb-4">Repeating Subjects</h2>
        <div class="space-y-4">
          <div v-for="(subject, index) in cgpaData.subjects" :key="index" class="bg-slate-50 p-4 rounded-lg border border-slate-200 relative">
            <h3 class="font-semibold text-slate-600 mb-2">Subject {{ index + 1 }}</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label :for="`subj-credit-${index}`" class="block text-sm font-medium text-slate-600 mb-1">Credit Hours</label>
                <input type="number" :id="`subj-credit-${index}`" v-model.number="subject.credit" min="0" step="1" class="w-full p-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-indigo-500"/>
              </div>
              <div>
                <label :for="`old-grade-${index}`" class="block text-sm font-medium text-slate-600 mb-1">Old Grade</label>
                <select :id="`old-grade-${index}`" v-model="subject.old_grade" class="w-full p-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-indigo-500">
                  <option v-for="grade in GRADES" :value="grade" :key="grade">{{ grade }}</option>
                </select>
              </div>
              <div>
                <label :for="`new-grade-${index}`" class="block text-sm font-medium text-slate-600 mb-1">New Grade</label>
                <select :id="`new-grade-${index}`" v-model="subject.new_grade" class="w-full p-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-indigo-500">
                  <option v-for="grade in GRADES" :value="grade" :key="grade">{{ grade }}</option>
                </select>
              </div>
            </div>
             <button type="button" @click="removeSubject(index)" v-if="cgpaData.subjects.length > 1" class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full h-6 w-6 flex items-center justify-center font-bold text-xs hover:bg-red-600 transition">&times;</button>
          </div>
        </div>
        
        <div class="flex items-center space-x-4 mt-6">
          <button type="button" @click="addSubject" class="w-full bg-slate-200 text-slate-700 cursor-pointer font-semibold py-3 px-4 rounded-lg hover:bg-slate-300 transition">
            + Add Subject
          </button>
          <button type="submit" :disabled="isLoading" class="w-full bg-indigo-600 text-white cursor-pointer font-bold py-3 px-4 rounded-lg hover:bg-indigo-700 disabled:bg-indigo-300 disabled:cursor-not-allowed transition">
            <span v-if="isLoading">Calculating...</span>
            <span v-else>Calculate New CGPA</span>
          </button>
        </div>

        <div v-if="resultCgpa !== null" class="mt-8 p-6 bg-green-50 border border-green-200 rounded-lg text-center">
          <p class="text-slate-600">Estimated New CGPA</p>
          <p class="text-4xl font-bold text-green-700">{{ resultCgpa.toFixed(2) }}</p>
        </div>
        <div v-if="error" class="mt-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg text-center">
          {{ error }}
        </div>

      </form>
    </div>
  </div>
</template>