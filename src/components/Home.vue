<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card class="pa-5">
            <h1 class="display-1 text-center mb-5">Welcome to the Macros Detector Tool</h1>
            <p class="subtitle-1 text-center mb-5">
              This tool helps you analyze and understand legacy VBA macros.
              Upload your Excel files containing macros, and let our advanced
              analysis tool provide detailed documentation and insights.
            </p>
  
            <FileUpload
              @fileProcessed="handleFileProcessed"
              @fileProcessingError="handleFileProcessingError"
              @clearResults="clearResults"
            />
  
            <v-alert v-if="result" type="success" class="mt-3">
              <pre>{{ result }}</pre>
            </v-alert>
            <v-alert v-if="error" type="error" class="mt-3">
              {{ error }}
            </v-alert>
          </v-card>
        </v-col>
      </v-row>
  
      <v-row class="align-center justify-center text-center mt-5">
        <v-col cols="12">
          <v-divider></v-divider>
        </v-col>
      </v-row>
  
      <v-row class="align-center justify-center text-center mt-3">
        <v-col cols="12" md="8">
          <v-card class="pa-5">
            <v-card-title class="text-center mb-4">Features</v-card-title>
            <v-card-text>
              <v-row>
                <!-- Adding Features -->
                <v-col cols="12" md="4" class="feature-item">
                  <v-icon color="primary" large>mdi-file-document-outline</v-icon>
                  <p>Automatic Macro Detection</p>
                </v-col>
                <v-col cols="12" md="4" class="feature-item">
                  <v-icon color="primary" large>mdi-code-tags-check</v-icon>
                  <p>Detailed Analysis and Documentation</p>
                </v-col>
                <v-col cols="12" md="4" class="feature-item">
                  <v-icon color="primary" large>mdi-cogs</v-icon>
                  <p>Seamless Integration with Modern Technologies</p>
                </v-col>
                <v-col cols="12" md="4" class="feature-item">
                  <v-icon color="primary" large>mdi-function-variant</v-icon>
                  <p>Function Logic Describer</p>
                </v-col>
                <v-col cols="12" md="4" class="feature-item">
                  <v-icon color="primary" large>mdi-file-document-outline</v-icon>
                  <p>Document VBA Code</p>
                </v-col>
                <v-col cols="12" md="4" class="feature-item">
                  <v-icon color="primary" large>mdi-file-document-outline</v-icon>
                  <p>Visualize Logic Flowchart</p>
                </v-col>
                <v-col cols="12" md="4" class="feature-item">
                  <v-icon color="primary" large>mdi-speedometer</v-icon>
                  <p>Code Efficiency Evaluation</p>
                </v-col>
                <v-col cols="12" md="4" class="feature-item">
                  <v-icon color="primary" large>mdi-language-python</v-icon>
                  <p>Convert VBA to Python Code</p>
                </v-col>
                <v-col cols="12" md="4" class="feature-item">
                  <v-icon color="primary" large>mdi-link-variant</v-icon>
                  <p>Macro Dependency Mapping</p>
                </v-col>
                <v-col cols="12" md="4" class="feature-item">
                  <v-icon color="primary" large>mdi-tune</v-icon>
                  <p>Process Optimization</p>
                </v-col>
                <v-col cols="12" md="4" class="feature-item">
                  <v-icon color="primary" large>mdi-alert-circle-outline</v-icon>
                  <p>Error Detection and Correction</p>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import FileUpload from '../components/FileUploadPage.vue';
  
  export default {
    name: 'Home',
    components: {
      FileUpload,
    },
    data() {
      return {
        result: null,
        error: null,
      };
    },
    methods: {
      handleFileProcessed(result) {
        this.result = result;
        this.error = null;
      },
      handleFileProcessingError(error) {
        this.result = null;
        this.error = error;
      },
      clearResults() {
        this.result = null;
        this.error = null;
      },
    },
  };
  </script>
  
  <style scoped>
  .v-card {
    max-width: 1200px;
    margin: 0 auto;
    background-color: rgba(255, 255, 255, 0.9);
  }
  
  .feature-item {
    text-align: center;
    padding: 16px;
  }
  
  .feature-item p {
    margin-top: 8px;
  }
  
  .text-center {
    text-align: center;
  }
  
  .mt-5 {
    margin-top: 5rem;
  }
  </style>
  