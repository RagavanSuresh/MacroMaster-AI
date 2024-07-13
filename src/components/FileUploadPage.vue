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
              v-if="result"
              type="success"
              class="mt-3"
            >
              {{ result }}
            </v-alert>
            <v-alert
              v-if="error"
              type="error"
              class="mt-3"
            >
              {{ error }}
            </v-alert>
          </v-card>
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
      };
    },
    methods: {
      handleFileUpload() {
        this.result = null;
        this.error = null;
      },
      async submitFile() {
        if (!this.file) return;
  
        this.loading = true;
        const formData = new FormData();
        formData.append('file', this.file);
  
        try {
          const response = await axios.post('http://localhost:5000/api/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
          this.result = response.data.analysis;
        } catch (error) {
          console.error(error);
          this.error = 'Failed to process the file. Please try again.';
        } finally {
          this.loading = false;
        }
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
  </style>
  