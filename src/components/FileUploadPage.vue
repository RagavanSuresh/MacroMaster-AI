<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card class="pa-5">
            <v-file-input
              v-model="file"
              label="Upload your file (.xlsm only)"
              prepend-icon="mdi-upload"
              @change="handleFileUpload"
              accept=".xlsm"
            ></v-file-input>
            <v-btn @click="submitFile" :disabled="!file" class="mt-3" color="primary">
              Submit
            </v-btn>
            <v-progress-circular
              v-if="loading"
              indeterminate
              color="primary"
              class="ma-3"
            ></v-progress-circular>
            <v-alert
              v-if="error"
              type="error"
              class="mt-3"
            >
              {{ error }}
            </v-alert>
            <v-alert
              v-if="result"
              type="success"
              class="mt-3"
            >
              Result successfully generated.
            </v-alert>
          </v-card>

          <v-row v-if="result && result.security_vulnerabilities" class="mt-3" justify="center">
            <v-col cols="12">
              <v-card :class="securityCardClass">
                <v-card-title class="d-flex justify-center">
                  <v-icon class="mr-2">mdi-shield-alert</v-icon>
                  Security Vulnerabilities
                </v-card-title>
                <v-card-text class="text-center card-content">
                  {{ result.security_vulnerabilities }}
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
  
          <!-- Cards Display -->
          <v-row v-if="result" class="mt-3" justify="center">
            <v-col cols="12" md="6" v-for="(value, key) in filteredResult" :key="key">
              <v-card class="result-card" @click="showDialog(key, value)">
                <v-card-title class="d-flex justify-center">
                  <v-icon class="mr-2">{{ getIcon(key) }}</v-icon>
                  <span class="card-text">{{ formatKey(key) }}</span>
                </v-card-title>
                <v-card-text class="card-description">
                  <span class="description-text">{{ getDescription(key) }}</span>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
  
          <!-- Security Vulnerabilities Card -->
          
  
          <!-- Dialog for Detailed View -->
          <v-dialog v-model="dialog" max-width="600px">
            <v-card>
              <v-card-title class="headline">{{ dialogTitle }}</v-card-title>
              <v-card-text>
                <pre v-if="dialogTitle !== 'Process Flowchart Generator'">{{ dialogContent }}</pre>
                <img v-else :src="flowchartUrl" alt="Flowchart" class="mt-3" />
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="dialog = false">Close</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  
  <script>
import axios from 'axios';

export default {
  data() {
    return {
      file: null,
      result: null,
      error: null,
      loading: false,
      dialog: false,
      dialogTitle: '',
      dialogContent: '',
      flowchartUrl: 'flowchart.png', // Path to the generated flowchart image
    };
  },
  methods: {
    handleFileUpload() {
      this.error = null;
      this.result = null; // Reset result on new upload
    },
    async submitFile() {
      if (!this.file) return;

      this.loading = true;
      const formData = new FormData();
      formData.append('file', this.file);

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        // Set result from response
        this.result = response.data;
      } catch (error) {
        console.error(error);
        this.error = 'Failed to process the file. Please try again.';
      } finally {
        this.loading = false;
      }
    },
    showDialog(key, value) {
      this.dialogTitle = this.formatKey(key);
      this.dialogContent = key === 'logic_flowchart' ? '' : value;
      this.dialog = true;
    },
    formatKey(key) {
      const keyMap = {
        functionalLogic: 'Function Logic Describer',
        documented_code: 'Document VBA Code',
        logic_flowchart: 'Process Flowchart Generator',
        code_efficiency: 'Enhance Code Efficiency',
        python_code: 'Python Code Converter',
        macro_dependency: 'Generate Macro Dependency',
        Process_optimizer: 'Optimize Process',
        Error_detector_corrector: 'Smart Code Fix',
      };
      return keyMap[key] || key;
    },
    getDescription(key) {
      const descriptionMap = {
        functionalLogic: 'Extract and explain the functional logic embedded within VBA macros.',
        documented_code: 'Automatically analyze Excel VBA macros to create comprehensive documentation of their logic, data flow, and process flow.',
        logic_flowchart: 'Visualize the process flow of VBA macros with flowcharts.',
        code_efficiency: 'Evaluate the quality and efficiency of VBA macros.',
        python_code: 'Convert VBA macros to modern Python code with refactoring recommendations for improved performance and maintainability.',
        macro_dependency: 'Map dependencies between different VBA macros and Excel files.',
        Process_optimizer: 'Analyze the data flow within VBA macros to identify bottlenecks and optimization opportunities.',
        Error_detector_corrector: 'Detect and correct errors in VBA macros.',
      };
      return descriptionMap[key] || '';
    },
    getIcon(key) {
      const iconMap = {
        functionalLogic: 'mdi-function-variant',
        documented_code: 'mdi-file-document-outline',
        logic_flowchart: 'mdi-code-tags-check',
        code_efficiency: 'mdi-speedometer',
        python_code: 'mdi-language-python',
        macro_dependency: 'mdi-cogs',
        Process_optimizer: 'mdi-tune',
        Error_detector_corrector: 'mdi-alert-circle-outline',
      };
      return iconMap[key] || 'mdi-file';
    },
  },
  computed: {
    filteredResult() {
      if (this.result) {
        const { security_vulnerabilities, ...rest } = this.result;
        return rest;
      }
      return {};
    },
    securityCardClass() {
      if (this.result && this.result.security_vulnerabilities) {
        return this.result.security_vulnerabilities.toLowerCase() === 'no' ? 'green-card' : 'red-card';
      }
      return '';
    },
  },
};
</script>

  
<style scoped>
.v-card {
  max-width: 800px;
  margin: 0 auto;
}
.v-alert {
  text-align: center;
}
.result-card {
  cursor: pointer;
  min-height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s;
  text-align: center;
  padding: 16px;
  overflow: hidden;
  position: relative;
  position: relative;
}
.result-card:hover {
  transform: scale(1.05);
}
.card-text {
  font-size: 12px; /* Reduced font size */
  word-wrap: break-word; /* Ensure text wraps */
  word-break: break-all; /* Ensure text wraps */
  white-space: pre-wrap; /* Ensure text wraps */
  padding: 10px; /* Added padding */
}
.card-description {
  display: none;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 16px;
  box-sizing: border-box;
  text-align: left;
  font-size: 12px; /* Adjust font size as needed */
}
.result-card:hover .card-description {
  display: block;
}
.green-card {
  background-color: #d4edda;
  color: #155724;
}
.red-card {
  background-color: #f8d7da;
  color: #721c24;
}
.text-wrap {
  word-wrap: break-word; /* Ensure text wraps */
  word-break: break-all; /* Ensure text wraps */
  white-space: pre-wrap; /* Ensure text wraps */
}
pre {
  text-align: left;
  white-space: pre-wrap; /* Ensure preformatted text wraps */
}
img {
  max-width: 100%;
  height: auto;
}
</style>
