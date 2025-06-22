// YouTube Analytics AI Backend - JavaScript Test Script
// Tests all API endpoints using fetch API

const BASE_URL = 'http://localhost:8000';
const TEST_VIDEO_ID = 'dQw4w9WgXcQ';
const TEST_CHANNEL_ID = 'UC_x5XG1OV2P6uZZ5FSM9Ttw';

// Utility function to make API calls
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, options);
        const result = await response.json();
        return { status: response.status, data: result };
    } catch (error) {
        return { status: 'error', data: { error: error.message } };
    }
}

// Test functions
async function testHealthCheck() {
    console.log('1. Testing Health Check...');
    const result = await apiCall('/health');
    console.log('Health Check Result:', result);
    return result.status === 200;
}

async function testAgentCapabilities() {
    console.log('2. Testing Agent Capabilities...');
    const result = await apiCall('/api/agents');
    console.log('Agent Capabilities Result:', result);
    return result.status === 200;
}

async function testWorkflowStatus() {
    console.log('3. Testing Workflow Status...');
    const result = await apiCall('/api/workflow', 'POST');
    console.log('Workflow Status Result:', result);
    return result.status === 200;
}

async function testVideoAnalytics() {
    console.log('4. Testing Video Analytics...');
    const result = await apiCall('/api/analytics', 'POST', {
        video_id: TEST_VIDEO_ID
    });
    console.log('Video Analytics Result:', result);
    return result.status === 200;
}

async function testCommentsAnalysis() {
    console.log('5. Testing Comments Analysis...');
    const result = await apiCall('/api/comments', 'POST', {
        video_id: TEST_VIDEO_ID
    });
    console.log('Comments Analysis Result:', result);
    return result.status === 200;
}

async function testTranscriptAnalysis() {
    console.log('6. Testing Transcript Analysis...');
    const result = await apiCall('/api/transcript', 'POST', {
        video_id: TEST_VIDEO_ID
    });
    console.log('Transcript Analysis Result:', result);
    return result.status === 200;
}

async function testChannelAnalysis() {
    console.log('7. Testing Channel Analysis...');
    const result = await apiCall('/api/channel', 'POST', {
        channel_id: TEST_CHANNEL_ID
    });
    console.log('Channel Analysis Result:', result);
    return result.status === 200;
}

async function testVideoComparison() {
    console.log('8. Testing Video Comparison...');
    const result = await apiCall('/api/compare', 'POST', {
        video_ids: [TEST_VIDEO_ID, '9bZkp7q19f0', 'kJQP7kiw5Fk']
    });
    console.log('Video Comparison Result:', result);
    return result.status === 200;
}

async function testContentGeneration() {
    console.log('9. Testing Content Generation...');
    const mockAnalytics = {
        video_analytics: {
            basic_info: {
                title: 'Test Video',
                view_count: 1000000,
                like_count: 50000
            }
        },
        comment_analysis: {
            total_comments: 2000,
            sentiment_breakdown: {
                positive: 1200,
                negative: 200,
                neutral: 600
            }
        },
        transcript_analysis: {
            word_count: 1500,
            ai_analysis: 'This is a test video analysis.'
        }
    };
    
    const result = await apiCall('/api/content', 'POST', {
        analytics_data: mockAnalytics,
        content_type: 'social_post'
    });
    console.log('Content Generation Result:', result);
    return result.status === 200;
}

async function testContentCritique() {
    console.log('10. Testing Content Critique...');
    const mockContent = {
        content: 'This is a test social media post about our latest video. Check it out!',
        image_prompt: 'A professional image showing analytics dashboard'
    };
    
    const result = await apiCall('/api/critique', 'POST', {
        content: mockContent,
        content_type: 'social_post'
    });
    console.log('Content Critique Result:', result);
    return result.status === 200;
}

async function testFullAnalysis(workflowSteps, contentType = 'social_post') {
    console.log(`11. Testing Full Analysis with steps: ${workflowSteps.join(', ')}...`);
    const result = await apiCall('/api/analyze', 'POST', {
        video_id: TEST_VIDEO_ID,
        workflow_steps: workflowSteps,
        content_type: contentType
    });
    console.log('Full Analysis Result:', result);
    return result.status === 200;
}

async function testErrorHandling() {
    console.log('12. Testing Error Handling...');
    
    // Test invalid video ID
    const invalidResult = await apiCall('/api/analytics', 'POST', {
        video_id: 'invalid_video_id'
    });
    console.log('Invalid Video ID Result:', invalidResult);
    
    // Test missing video ID
    const missingResult = await apiCall('/api/analytics', 'POST', {});
    console.log('Missing Video ID Result:', missingResult);
    
    return true;
}

async function testDifferentContentTypes() {
    console.log('13. Testing Different Content Types...');
    const contentTypes = ['social_post', 'blog_post', 'newsletter', 'tweet'];
    
    for (const contentType of contentTypes) {
        console.log(`Testing content type: ${contentType}`);
        const result = await apiCall('/api/analyze', 'POST', {
            video_id: TEST_VIDEO_ID,
            workflow_steps: ['analytics', 'content'],
            content_type: contentType
        });
        console.log(`${contentType} Result:`, result.status);
    }
    
    return true;
}

async function testTaskManagement() {
    console.log('16. Testing Task Management...');
    
    // Start a task with content generation
    const result = await apiCall('/api/analyze', 'POST', {
        video_id: TEST_VIDEO_ID,
        workflow_steps: ['analytics', 'content'],
        content_type: 'social_post'
    });
    
    console.log('Task Management Result:', result);
    
    if (result.status === 200 && result.data.task_id) {
        const taskId = result.data.task_id;
        console.log(`Task ID: ${taskId}`);
        
        // Check task status
        const statusResult = await apiCall(`/api/task/${taskId}`);
        console.log('Task Status Result:', statusResult);
        
        // Wait and check again
        console.log('Waiting 5 seconds and checking again...');
        await new Promise(resolve => setTimeout(resolve, 5000));
        
        const statusResult2 = await apiCall(`/api/task/${taskId}`);
        console.log('Task Status After Wait Result:', statusResult2);
    }
    
    return result.status === 200;
}

async function testListTasks() {
    console.log('17. Testing List Tasks...');
    const result = await apiCall('/api/tasks');
    console.log('List Tasks Result:', result);
    return result.status === 200;
}

async function testContentGenerationWithTask() {
    console.log('18. Testing Content Generation with Task...');
    
    const result = await apiCall('/api/content', 'POST', {
        video_id: TEST_VIDEO_ID,
        content_type: 'social_post'
    });
    
    console.log('Content Generation with Task Result:', result);
    
    if (result.status === 200 && result.data.task_id) {
        const taskId = result.data.task_id;
        console.log(`Content Task ID: ${taskId}`);
        
        // Monitor content generation
        console.log('Waiting for content generation to complete...');
        const maxWait = 30; // 30 seconds max
        let waitTime = 0;
        
        while (waitTime < maxWait) {
            await new Promise(resolve => setTimeout(resolve, 2000));
            waitTime += 2;
            
            const statusResult = await apiCall(`/api/task/${taskId}`);
            if (statusResult.status === 200) {
                if (statusResult.data.status === 'completed') {
                    console.log('Content Generation Completed:', statusResult.data);
                    return true;
                } else if (statusResult.data.status === 'failed') {
                    console.log('Content Generation Failed:', statusResult.data);
                    return false;
                }
            }
            
            console.log(`Still processing... (${waitTime}s)`);
        }
        
        console.log('Task timed out');
        return false;
    }
    
    return result.status === 200;
}

async function testCleanupTasks() {
    console.log('19. Testing Cleanup Tasks...');
    const result = await apiCall('/api/tasks/cleanup', 'POST');
    console.log('Cleanup Tasks Result:', result);
    return result.status === 200;
}

// Main test runner
async function runAllTests() {
    console.log('🚀 Starting YouTube Analytics AI Backend Tests');
    console.log(`Base URL: ${BASE_URL}`);
    console.log(`Test Video ID: ${TEST_VIDEO_ID}`);
    console.log('==========================================');
    
    const tests = [
        { name: 'Health Check', fn: testHealthCheck },
        { name: 'Agent Capabilities', fn: testAgentCapabilities },
        { name: 'Workflow Status', fn: testWorkflowStatus },
        { name: 'Video Analytics', fn: testVideoAnalytics },
        { name: 'Comments Analysis', fn: testCommentsAnalysis },
        { name: 'Transcript Analysis', fn: testTranscriptAnalysis },
        { name: 'Channel Analysis', fn: testChannelAnalysis },
        { name: 'Video Comparison', fn: testVideoComparison },
        { name: 'Content Generation', fn: testContentGeneration },
        { name: 'Content Critique', fn: testContentCritique },
        { name: 'Full Analysis - Analytics Only', fn: () => testFullAnalysis(['analytics']) },
        { name: 'Full Analysis - Analytics + Content', fn: () => testFullAnalysis(['analytics', 'content']) },
        { name: 'Full Analysis - Complete Workflow', fn: () => testFullAnalysis(['analytics', 'content', 'critique']) },
        { name: 'Error Handling', fn: testErrorHandling },
        { name: 'Different Content Types', fn: testDifferentContentTypes },
        { name: 'Task Management', fn: testTaskManagement },
        { name: 'List Tasks', fn: testListTasks },
        { name: 'Content Generation with Task', fn: testContentGenerationWithTask },
        { name: 'Cleanup Tasks', fn: testCleanupTasks }
    ];
    
    const results = [];
    
    for (const test of tests) {
        console.log(`\n⏳ Running: ${test.name}`);
        const startTime = Date.now();
        
        try {
            const success = await test.fn();
            const endTime = Date.now();
            const duration = (endTime - startTime) / 1000;
            
            const status = success ? '✅ PASS' : '❌ FAIL';
            results.push({ name: test.name, success, duration });
            
            console.log(`${status} - ${test.name} (${duration.toFixed(2)}s)`);
            
        } catch (error) {
            const endTime = Date.now();
            const duration = (endTime - startTime) / 1000;
            results.push({ name: test.name, success: false, duration });
            console.log(`❌ FAIL - ${test.name} (${duration.toFixed(2)}s) - Exception: ${error.message}`);
        }
    }
    
    // Summary
    console.log('\n==========================================');
    console.log('TEST SUMMARY');
    console.log('==========================================');
    
    const passed = results.filter(r => r.success).length;
    const total = results.length;
    const totalTime = results.reduce((sum, r) => sum + r.duration, 0);
    
    console.log(`Total Tests: ${total}`);
    console.log(`Passed: ${passed}`);
    console.log(`Failed: ${total - passed}`);
    console.log(`Success Rate: ${((passed/total)*100).toFixed(1)}%`);
    console.log(`Total Time: ${totalTime.toFixed(2)}s`);
    
    console.log('\nDetailed Results:');
    results.forEach(result => {
        const status = result.success ? '✅ PASS' : '❌ FAIL';
        console.log(`  ${status} - ${result.name} (${result.duration.toFixed(2)}s)`);
    });
    
    if (passed === total) {
        console.log('\n🎉 ALL TESTS PASSED!');
    } else {
        console.log(`\n⚠️  ${total - passed} TESTS FAILED`);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        apiCall,
        runAllTests,
        testHealthCheck,
        testVideoAnalytics,
        testFullAnalysis
    };
}

// Run tests if this file is executed directly
if (typeof window === 'undefined') {
    // Node.js environment
    runAllTests().catch(console.error);
} else {
    // Browser environment
    console.log('Run runAllTests() to start testing');
}