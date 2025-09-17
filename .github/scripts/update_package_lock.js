#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

/**
 * Update version in package-lock.json
 * @param {string} filePath - Path to package-lock.json file
 * @param {string} newVersion - New version to set (e.g., 'v1.0.1' or '1.0.1')
 * @returns {boolean} - True if update was successful, false otherwise
 */
const updatePackageLockVersion = (filePath, newVersion) => {
    try {
        // Read package-lock.json
        const content = fs.readFileSync(filePath, 'utf8');
        const data = JSON.parse(content);
        
        // Remove 'v' prefix if present
        const cleanVersion = newVersion.replace(/^v/, '');
        
        // Update version in root package
        const oldVersion = data.version || 'unknown';
        data.version = cleanVersion;
        
        // Update version in packages[""] if it exists (npm v7+)
        if (data.packages && data.packages[""]) {
            data.packages[""].version = cleanVersion;
        }
        
        // Write back to file with proper formatting
        fs.writeFileSync(filePath, JSON.stringify(data, null, 2) + '\n');
        
        console.log(`>>Updated version from ${oldVersion} to ${cleanVersion} in ${filePath}`);
        return true;
        
    } catch (error) {
        if (error.code === 'ENOENT') {
            console.log(`>>Error: File ${filePath} not found`);
        } else if (error instanceof SyntaxError) {
            console.log(`>>Error: Invalid JSON in ${filePath}: ${error.message}`);
        } else {
            console.log(`>>Error updating ${filePath}: ${error.message}`);
        }
        return false;
    }
}

function main() {
    const args = process.argv.slice(2);
    
    // Handle help argument
    if (args.includes('--help') || args.includes('-h')) {
        console.log('Usage: node update_package_lock.js <version> [--file <path>]');
        console.log('');
        console.log('Update version in package-lock.json');
        console.log('');
        console.log('Arguments:');
        console.log('  version      New version (e.g., v1.0.1 or 1.0.1)');
        console.log('');
        console.log('Options:');
        console.log('  --file FILE  Path to package-lock.json file');
        process.exit(0);
    }
    
    if (args.length === 0) {
        console.log('>>Usage: node update_package_lock.js <version> [--file <path>]');
        console.log('>>Example: node update_package_lock.js v1.0.1');
        process.exit(1);
    }
    
    let version = args[0];
    let filePath = 'package-lock.json';
    
    // Parse arguments
    for (let i = 1; i < args.length; i++) {
        if (args[i] === '--file' && i + 1 < args.length) {
            filePath = args[i + 1];
            i++; // Skip next argument
        }
    }
    
    const success = updatePackageLockVersion(filePath, version);
    process.exit(success ? 0 : 1);
}

if (require.main === module) {
    main();
}