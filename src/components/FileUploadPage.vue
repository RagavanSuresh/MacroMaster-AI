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
                  Security Vulnerabilities
                </v-card-title>
                <v-card-text class="text-center">
                  {{ result.security_vulnerabilities }}
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
  
          <v-row v-if="result" class="mt-3" justify="center">
            <v-col cols="12" md="6" v-for="(value, key) in filteredResult" :key="key">
              <v-hover v-slot:default="{ isHovering }">
                <v-card class="result-card" @click="showDialog(key, value)">
                  <v-card-title class="d-flex justify-center">
                    {{ key }}
                  </v-card-title>
                  <v-expand-transition>
                    <v-card-text v-show="isHovering && key !== 'logic_flowchart'" class="text-center">
                      {{ value }}
                    </v-card-text>
                    <v-card-text v-show="isHovering && key === 'logic_flowchart'" class="text-center">
                      <img :src="flowchartUrl" alt="Flowchart" class="mt-3" />
                    </v-card-text>
                  </v-expand-transition>
                </v-card>
              </v-hover>
            </v-col>
          </v-row>
  
          
  
          <v-dialog v-model="dialog" max-width="600px">
            <v-card>
              <v-card-title class="headline">{{ dialogTitle }}</v-card-title>
              <v-card-text>
                <pre v-if="dialogTitle !== 'logic_flowchart'">{{ dialogContent }}</pre>
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
        this.dialogTitle = key;
        this.dialogContent = key === 'logic_flowchart' ? '' : value;
        this.dialog = true;
      },
    },
    computed: {
      filteredResult() {
        if (!this.result) return {};
        const { security_vulnerabilities, ...rest } = this.result;
        return rest;
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
  }
  .result-card:hover {
    transform: scale(1.05);
  }
  .green-card {
    background-color: #d4edda;
    color: #155724;
  }
  .red-card {
    background-color: #f8d7da;
    color: #721c24;
  }
  pre {
    text-align: left;
    white-space: pre-wrap; /* Make sure preformatted text wraps */
  }
  img {
    max-width: 100%;
    height: auto;
  }
  </style>
  