const express = require('express');
const bodyParser = require('body-parser');
const awsServerlessExpressMiddleware = require('aws-serverless-express/middleware');
const AWS = require('aws-sdk');
const cors = require('cors');

// Initialize Express app
const app = express();

// Configure middleware
app.use(bodyParser.json());
app.use(awsServerlessExpressMiddleware.eventContext());
app.use(cors());

// Enable CORS for all methods
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "*");
  next();
});

// Initialize DynamoDB client
const docClient = new AWS.DynamoDB.DocumentClient();
const tableName = process.env.AUDIT_TABLE || 'EchoGuardAuditLogs';

// GET /audit-logs - Retrieve audit logs with optional filtering
app.get('/audit-logs', async function(req, res) {
  try {
    // Get query parameters for filtering
    const { minScore, maxScore, startDate, endDate, limit } = req.query;
    
    // Base params
    const params = {
      TableName: tableName,
      Limit: limit ? parseInt(limit) : 100
    };
    
    // Add filters if provided
    if (minScore || maxScore || startDate || endDate) {
      let filterExpressions = [];
      let expressionAttributeValues = {};
      
      if (minScore) {
        filterExpressions.push('score >= :minScore');
        expressionAttributeValues[':minScore'] = parseInt(minScore);
      }
      
      if (maxScore) {
        filterExpressions.push('score <= :maxScore');
        expressionAttributeValues[':maxScore'] = parseInt(maxScore);
      }
      
      if (startDate) {
        filterExpressions.push('timestamp >= :startDate');
        expressionAttributeValues[':startDate'] = startDate;
      }
      
      if (endDate) {
        filterExpressions.push('timestamp <= :endDate');
        expressionAttributeValues[':endDate'] = endDate;
      }
      
      params.FilterExpression = filterExpressions.join(' AND ');
      params.ExpressionAttributeValues = expressionAttributeValues;
    }
    
    const data = await docClient.scan(params).promise();
    
    // Sort by timestamp descending (newest first)
    const sortedItems = data.Items.sort((a, b) => {
      return new Date(b.timestamp) - new Date(a.timestamp);
    });
    
    res.json(sortedItems);
  } catch (err) {
    console.error('Error retrieving audit logs:', err);
    res.status(500).json({ 
      error: 'Could not load audit logs', 
      details: err.message 
    });
  }
});

// GET /audit-logs/stats - Get statistics about compliance logs
app.get('/audit-logs/stats', async function(req, res) {
  try {
    const params = {
      TableName: tableName
    };
    
    const data = await docClient.scan(params).promise();
    const items = data.Items;
    
    // Calculate statistics
    const stats = {
      totalCalls: items.length,
      averageScore: 0,
      complianceIssues: 0,
      toneBreakdown: {},
      commonFlags: {}
    };
    
    if (items.length > 0) {
      // Calculate average score
      const totalScore = items.reduce((sum, item) => sum + (item.score || 0), 0);
      stats.averageScore = Math.round(totalScore / items.length);
      
      // Count compliance issues (score < 70)
      stats.complianceIssues = items.filter(item => (item.score || 0) < 70).length;
      
      // Count tone occurrences
      items.forEach(item => {
        const tone = item.tone || 'unknown';
        stats.toneBreakdown[tone] = (stats.toneBreakdown[tone] || 0) + 1;
      });
      
      // Count flag occurrences
      items.forEach(item => {
        const flags = item.flags || [];
        flags.forEach(flag => {
          stats.commonFlags[flag] = (stats.commonFlags[flag] || 0) + 1;
        });
      });
    }
    
    res.json(stats);
  } catch (err) {
    console.error('Error retrieving audit log statistics:', err);
    res.status(500).json({ 
      error: 'Could not load audit log statistics', 
      details: err.message 
    });
  }
});

// GET /audit-logs/:callId - Retrieve a specific audit log
app.get('/audit-logs/:callId', async function(req, res) {
  try {
    const params = {
      TableName: tableName,
      Key: {
        callId: req.params.callId
      }
    };
    
    const data = await docClient.get(params).promise();
    
    if (data.Item) {
      res.json(data.Item);
    } else {
      res.status(404).json({ error: 'Audit log not found' });
    }
  } catch (err) {
    console.error('Error retrieving audit log:', err);
    res.status(500).json({ 
      error: 'Could not retrieve audit log', 
      details: err.message 
    });
  }
});

// POST /upload-url - Generate a pre-signed URL for direct S3 upload
app.post('/upload-url', async function(req, res) {
  try {
    // Validate request body
    const { fileName, fileType } = req.body;
    if (!fileName || !fileType) {
      return res.status(400).json({ error: 'fileName and fileType are required' });
    }
    
    // Get the audio bucket name from environment variable
    const audioBucket = process.env.AUDIO_BUCKET || '';
    if (!audioBucket) {
      return res.status(500).json({ error: 'Audio bucket not configured' });
    }
    
    // Generate a unique file key
    const fileKey = `uploads/${Date.now()}-${fileName}`;
    
    // Create S3 client
    const s3 = new AWS.S3();
    
    // Generate pre-signed URL
    const s3Params = {
      Bucket: audioBucket,
      Key: fileKey,
      ContentType: fileType,
      Expires: 300 // URL expires in 5 minutes
    };
    
    const uploadURL = s3.getSignedUrl('putObject', s3Params);
    
    res.json({
      uploadURL,
      fileKey
    });
  } catch (err) {
    console.error('Error generating upload URL:', err);
    res.status(500).json({ 
      error: 'Could not generate upload URL', 
      details: err.message 
    });
  }
});

// Error handler
app.use(function(err, req, res, next) {
  console.error(err.stack);
  res.status(500).json({
    error: 'Internal Server Error',
    details: err.message
  });
});

// Export the app
module.exports = app;