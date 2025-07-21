/**
 * EchoGuard API Client
 * 
 * This module provides functions to interact with the EchoGuard API.
 */

// API configuration
const API_CONFIG = {
  // Real API URL from CloudFormation deployment
  apiUrl: 'https://nqfzeccch0.execute-api.us-east-1.amazonaws.com/dev',
  
  // For demo mode, set to true to use simulated responses
  // Set to false to use the real backend
  demoMode: true // Using demo mode due to CORS issues
};

/**
 * Get authentication token from Cognito
 * @returns {string} The JWT token
 */
async function getAuthToken() {
  return new Promise((resolve, reject) => {
    const cognitoUser = userPool.getCurrentUser();
    
    if (!cognitoUser) {
      reject(new Error('No user logged in'));
      return;
    }
    
    cognitoUser.getSession((err, session) => {
      if (err) {
        reject(err);
        return;
      }
      
      if (session && session.isValid()) {
        resolve(session.getIdToken().getJwtToken());
      } else {
        reject(new Error('Invalid session'));
      }
    });
  });
}

/**
 * Make an authenticated API request
 * @param {string} path - API path
 * @param {string} method - HTTP method
 * @param {object} body - Request body (for POST/PUT)
 * @returns {Promise<object>} Response data
 */
async function apiRequest(path, method = 'GET', body = null) {
  if (API_CONFIG.demoMode) {
    return simulateApiResponse(path, method, body);
  }
  
  try {
    const token = await getAuthToken();
    
    const options = {
      method,
      headers: {
        'Authorization': token,
        'Content-Type': 'application/json'
      },
      mode: 'cors',
      credentials: 'same-origin'
    };
    
    if (body && (method === 'POST' || method === 'PUT')) {
      options.body = JSON.stringify(body);
    }
    
    console.log(`Making API request to: ${API_CONFIG.apiUrl}${path}`);
    console.log('Request options:', JSON.stringify(options));
    
    const response = await fetch(`${API_CONFIG.apiUrl}${path}`, options);
    
    if (!response.ok) {
      console.error(`API error: ${response.status} ${response.statusText}`);
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

/**
 * Get recordings for the current user
 * @param {number} limit - Maximum number of recordings to return
 * @param {string} nextToken - Pagination token
 * @returns {Promise<object>} Recordings data
 */
async function getRecordings(limit = 10, nextToken = null) {
  const userId = userPool.getCurrentUser().username;
  let path = `/users/${userId}/recordings?limit=${limit}`;
  
  if (nextToken) {
    path += `&nextToken=${encodeURIComponent(nextToken)}`;
  }
  
  return apiRequest(path);
}

/**
 * Get details for a specific recording
 * @param {string} recordingId - Recording ID
 * @returns {Promise<object>} Recording details
 */
async function getRecordingDetails(recordingId) {
  const userId = userPool.getCurrentUser().username;
  return apiRequest(`/users/${userId}/recordings/${recordingId}`);
}

/**
 * Request a pre-signed URL for uploading an audio file
 * @param {string} fileName - File name
 * @param {string} fileType - File MIME type
 * @param {string} description - Recording description
 * @returns {Promise<object>} Upload URL and recording ID
 */
async function requestUploadUrl(fileName, fileType, description) {
  const userId = userPool.getCurrentUser().username;
  
  return apiRequest(`/users/${userId}/recordings/upload`, 'POST', {
    userId,
    fileName,
    fileType,
    description
  });
}

/**
 * Upload a file using a pre-signed URL
 * @param {string} uploadUrl - Pre-signed S3 URL
 * @param {File} file - File to upload
 * @returns {Promise<void>}
 */
async function uploadFile(uploadUrl, file) {
  if (API_CONFIG.demoMode) {
    // Simulate upload delay
    return new Promise(resolve => setTimeout(resolve, 1500));
  }
  
  try {
    console.log('Uploading to URL:', uploadUrl);
    console.log('File type:', file.type);
    console.log('File size:', file.size);
    
    const response = await fetch(uploadUrl, {
      method: 'PUT',
      body: file,
      headers: {
        'Content-Type': file.type
      },
      mode: 'cors'
    });
    
    console.log('Upload response status:', response.status);
    
    if (!response.ok) {
      console.error('Upload failed with status:', response.status);
      throw new Error(`Upload failed: ${response.status} ${response.statusText}`);
    }
    
    return true;
  } catch (error) {
    console.error('Upload error:', error);
    throw error;
  }
}

/**
 * Simulate API responses for demo mode
 * @param {string} path - API path
 * @param {string} method - HTTP method
 * @param {object} body - Request body
 * @returns {Promise<object>} Simulated response
 */
function simulateApiResponse(path, method, body) {
  // Simulate network delay
  return new Promise(resolve => {
    setTimeout(() => {
      if (path.includes('/recordings') && !path.includes('/upload') && method === 'GET') {
        // Simulate getRecordings response
        resolve({
          recordings: [
            {
              recordingId: 'rec-001',
              fileName: 'customer-call.mp3',
              description: 'Customer Call - John Smith',
              uploadDate: '2025-07-20',
              status: 'COMPLETED',
              complianceScore: 92
            },
            {
              recordingId: 'rec-002',
              fileName: 'investment-consultation.wav',
              description: 'Investment Consultation',
              uploadDate: '2025-07-19',
              status: 'COMPLETED',
              complianceScore: 78
            },
            {
              recordingId: 'rec-003',
              fileName: 'product-pitch.mp3',
              description: 'Product Pitch - New Client',
              uploadDate: '2025-07-18',
              status: 'COMPLETED',
              complianceScore: 58
            }
          ],
          pagination: {}
        });
      } else if (path.includes('/upload') && method === 'POST') {
        // Simulate requestUploadUrl response
        resolve({
          recordingId: `rec-${Date.now().toString().substr(-6)}`,
          uploadUrl: 'https://example.com/upload',
          message: 'Upload URL generated successfully'
        });
      } else if (path.match(/\/recordings\/rec-\w+$/) && method === 'GET') {
        // Simulate getRecordingDetails response
        const recordingId = path.split('/').pop();
        
        resolve({
          recording: {
            recordingId,
            fileName: body?.fileName || 'recording.mp3',
            description: body?.description || 'Audio Recording',
            uploadDate: new Date().toISOString().split('T')[0],
            status: 'COMPLETED',
            complianceScore: Math.floor(Math.random() * 36) + 60
          },
          analysis: {
            complianceScore: Math.floor(Math.random() * 36) + 60,
            issues: [
              {
                source: 'Bedrock',
                description: 'Missing required disclosure about investment risks',
                risk_level: 'High',
                recommendation: 'Include standard risk disclosure statement'
              },
              {
                source: 'Kiro AI',
                description: 'Potential misleading statement about expected returns',
                risk_level: 'Medium',
                recommendation: 'Clarify that past performance does not guarantee future results'
              }
            ],
            bedrockSummary: 'The conversation contains several compliance issues related to financial advice regulations.',
            kiroSummary: 'Multiple instances of non-compliant language detected in financial recommendations.'
          },
          transcript: 'This is a simulated transcript of the audio recording. In a real implementation, this would contain the actual text transcribed from the audio file.'
        });
      } else {
        // Default response
        resolve({
          message: 'Simulated API response',
          path,
          method,
          body
        });
      }
    }, 800);
  });
}

// Export API functions
window.echoGuardApi = {
  getRecordings,
  getRecordingDetails,
  requestUploadUrl,
  uploadFile
};