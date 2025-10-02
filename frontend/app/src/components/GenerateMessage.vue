<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-6 flex flex-col justify-center sm:py-12">
    <div class="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22%3E%3Crect width=%22100%22 height=%22100%22 fill=%22none%22/%3E%3Cpath d=%22M0 0l100 100M100 0L0 100%22 stroke-width=%220.2%22 stroke=%22%23ffffff10%22/%3E%3C/svg%3E')] bg-repeat [mask-image:radial-gradient(ellipse_at_center,white,transparent)] pointer-events-none"></div>
    <div class="relative py-3 sm:max-w-xl sm:mx-auto animate-float">
      <div class="absolute inset-0 bg-gradient-to-r from-blue-600/30 to-indigo-600/30 backdrop-blur-xl shadow-lg transform hover:scale-105 transition-all duration-500 sm:rounded-3xl"></div>
      <div class="relative px-4 py-10 bg-white/10 backdrop-blur-xl shadow-2xl sm:rounded-3xl sm:p-20 border border-white/20">
        <div class="max-w-md mx-auto">
          <div class="space-y-4">
            <h2 class="text-4xl font-bold mb-8 text-center text-white animate-gradient">WhatsApp Message Generator</h2>
              
            <div class="mb-6">
              <label class="block text-sm font-medium text-white mb-2">Name (Optional)</label>
              <input 
                type="text" 
                v-model="name" 
                class="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent backdrop-blur-xl text-white"
                placeholder="Enter recipient's name"
              />
            </div>

            <div class="mb-6">
              <label class="block text-sm font-medium text-white mb-2">Message Prompt</label>
              <textarea 
                v-model="prompt" 
                rows="4" 
                class="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent backdrop-blur-xl text-white"
                placeholder="Enter your message prompt here..."
              ></textarea>
            </div>

            <div class="flex justify-center">
              <button 
                @click="generateMessage" 
                class="relative px-8 py-4 bg-gradient-to-r from-blue-500 via-indigo-500 to-blue-600 text-white rounded-xl hover:scale-105 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transform transition-all duration-300 animate-pulse hover:animate-none shadow-xl hover:shadow-2xl backdrop-blur-sm"
                :disabled="isLoading"
              >
                <span class="relative z-10">{{ isLoading ? 'Generating...' : 'Generate Message' }}</span>
              </button>
            </div>

            <div v-if="generatedMessage" class="mt-8 animate-fade-in space-y-6">
              <div class="bg-white p-6 rounded-lg shadow-lg border border-gray-200">
                <h3 class="text-lg font-semibold text-gray-800 mb-3">Generated Message:</h3>
                <textarea 
                  v-model="displayMessage" 
                  rows="4" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                ></textarea>
                <div class="mt-4 flex justify-end space-x-3">
                  <button 
                    @click="copyToClipboard" 
                    class="flex items-center px-4 py-2 text-sm text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-all duration-200"
                  >
                    <span class="mr-2">{{ copied ? 'Copied!' : 'Copy' }}</span>
                    <svg v-if="!copied" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </button>
                  <button 
                    @click="saveChanges" 
                    class="px-4 py-2 text-sm text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-all duration-200"
                  >
                    Save Changes
                  </button>
                </div>
              </div>

              <!-- Broadcast Section -->
              <div class="bg-white p-6 rounded-lg shadow-lg border border-gray-200">
                <h3 class="text-lg font-semibold text-gray-800 mb-4">Send to WhatsApp</h3>
                <div class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Select Target Audience</label>
                    <select 
                      v-model="selectedAudienceType" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="db">From Database</option>
                      <option value="upload">Upload Numbers</option>
                      <option value="paste">Paste Numbers</option>
                    </select>
                  </div>

                  <!-- Database Selection -->
                  <div v-if="selectedAudienceType === 'db'" class="animate-fade-in">
                    <select 
                      v-model="selectedGroup" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="">Select a group</option>
                      <option v-for="group in groups" :key="group.id" :value="group.id">
                        {{ group.name }}
                      </option>
                    </select>
                  </div>

                  <!-- File Upload -->
                  <div v-if="selectedAudienceType === 'upload'" class="animate-fade-in">
                    <input 
                      type="file" 
                      @change="handleFileUpload" 
                      accept=".csv,.txt"
                      class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                    >
                  </div>

                  <!-- Paste Numbers -->
                  <div v-if="selectedAudienceType === 'paste'" class="animate-fade-in">
                    <textarea 
                      v-model="pastedNumbers" 
                      rows="4" 
                      placeholder="Enter phone numbers (one per line)"
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    ></textarea>
                  </div>

                  <button 
                    @click="broadcastMessage" 
                    :disabled="!canBroadcast"
                    class="w-full px-6 py-3 text-white bg-green-600 rounded-lg hover:bg-green-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                    Send to WhatsApp
                  </button>
                </div>
              </div>
            </div>

            <div v-if="error" class="mt-4 p-4 bg-red-500/10 text-red-200 rounded-xl border border-red-500/20">
              {{ error }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'GenerateMessage',
  data() {
    return {
      name: '',
      prompt: '',
      generatedMessage: '',
      isLoading: false,
      error: null,
      copied: false,
      showCopiedAnimation: false,
      // New data properties for broadcast functionality
      selectedAudienceType: 'db',
      selectedGroup: '',
      groups: [], // This will be populated from the backend
      pastedNumbers: '',
      uploadedFile: null,
      isBroadcasting: false
    }
  },
  computed: {
    displayMessage: {
      get() {
        if (!this.generatedMessage) return '';
        return this.name 
          ? this.generatedMessage.replace('{name}', this.name)
          : this.generatedMessage;
      },
      set(value) {
        this.generatedMessage = value;
      }
    },
    canBroadcast() {
      if (this.isBroadcasting) return false;
      if (!this.generatedMessage) return false;
      
      const type = this.selectedAudienceType;
    if (type === 'db') return !!this.selectedGroup;
    if (type === 'upload') return !!this.uploadedFile;
    if (type === 'paste') return !!this.pastedNumbers.trim();
    return false;
    }
  },
  async created() {
    try {
      // Fetch groups from backend when component is created
      const response = await axios.get('http://127.0.0.1:8000/groups');
      this.groups = response.data;
    } catch (err) {
      console.error('Failed to fetch groups:', err);
    }
  },
  methods: {
    async generateMessage() {
      if (!this.prompt.trim()) {
        this.error = 'Please enter a prompt';
        return;
      }
      
      this.isLoading = true;
      this.error = null;
      this.generatedMessage = '';
      
      try {
        const response = await axios.post('http://127.0.0.1:8000/generate-message', {
          prompt: this.prompt
        });
        
        this.generatedMessage = response.data.message;
      } catch (err) {
        this.error = 'Failed to generate message. Please try again.';
        console.error('Error:', err);
      } finally {
        this.isLoading = false;
      }
    },
    async copyToClipboard() {
      try {
        await navigator.clipboard.writeText(this.displayMessage);
        this.copied = true;
        this.showCopiedAnimation = true;
        
        setTimeout(() => {
          this.copied = false;
        }, 2000);
        
        setTimeout(() => {
          this.showCopiedAnimation = false;
        }, 1000);
      } catch (err) {
        console.error('Failed to copy:', err);
      }
    },
    async saveChanges() {
      // Save the edited message
      this.generatedMessage = this.displayMessage;
      // Show a success message or notification here
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // Check if it's a CSV or TXT file
        if (file.type === 'text/csv' || file.type === 'text/plain') {
          this.uploadedFile = file;
        } else {
          this.error = 'Please upload a CSV or TXT file';
          event.target.value = ''; // Clear the file input
        }
      }
    },
    async broadcastMessage() {
      if (!this.canBroadcast) return;
      
      this.isBroadcasting = true;
      this.error = null;
      
      try {
        let recipients;
        
        switch (this.selectedAudienceType) {
          case 'db':
            // Use the selected group ID
            recipients = { groupId: this.selectedGroup };
            break;
          case 'upload':
            // Handle file upload
            const formData = new FormData();
            formData.append('file', this.uploadedFile);
            recipients = { file: formData };
            break;
          case 'paste':
            // Process pasted numbers
            recipients = {
              numbers: this.pastedNumbers
                .split('\n')
                .map(n => n.trim())
                .filter(n => n)
            };
            break;
        }
        
        await axios.post('http://127.0.0.1:8000/broadcast-message', {
          message: this.displayMessage,
          recipients,
          type: this.selectedAudienceType
        });
        
        // Show success message
        this.error = null;
        // Add success notification here
        
      } catch (err) {
        this.error = 'Failed to broadcast message. Please try again.';
        console.error('Error:', err);
      } finally {
        this.isBroadcasting = false;
      }
    }
  }
}
</script>

<style>
@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0px);
  }
}

@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

.animate-gradient {
  animation: gradient 6s ease infinite;
  background-size: 200% 200%;
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.backdrop-blur-md {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
</style>
