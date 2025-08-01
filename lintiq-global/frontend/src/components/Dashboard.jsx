/**
 * Dashboard Component
 * Main user dashboard with file upload and analysis
 */

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Code, 
  Upload, 
  CreditCard, 
  Shield, 
  Brain, 
  FileText,
  AlertTriangle,
  CheckCircle,
  Loader2,
  LogOut,
  User,
  Zap,
  TrendingUp,
  Clock,
  Download
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { analysis, payments } from '../lib/api';

const Dashboard = () => {
  const { user, logout, refreshUser } = useAuth();
  const navigate = useNavigate();
  
  const [files, setFiles] = useState([]);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState('');
  const [creditPackages, setCreditPackages] = useState([]);
  const [loadingPackages, setLoadingPackages] = useState(false);

  useEffect(() => {
    loadCreditPackages();
  }, []);

  const loadCreditPackages = async () => {
    try {
      setLoadingPackages(true);
      const response = await payments.getPackages();
      if (response.data.success) {
        setCreditPackages(response.data.packages);
      }
    } catch (error) {
      console.error('Failed to load credit packages:', error);
    } finally {
      setLoadingPackages(false);
    }
  };

  const handleFileSelect = (event) => {
    const selectedFiles = Array.from(event.target.files);
    setFiles(selectedFiles);
    setError('');
    setAnalysisResult(null);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const droppedFiles = Array.from(event.dataTransfer.files);
    setFiles(droppedFiles);
    setError('');
    setAnalysisResult(null);
  };

  const handleAnalyze = async () => {
    if (files.length === 0) {
      setError('Please select files to analyze');
      return;
    }

    setAnalyzing(true);
    setError('');

    try {
      const formData = new FormData();
      files.forEach(file => {
        formData.append('files', file);
      });
      formData.append('use_ai', user?.is_pro ? 'true' : 'false');

      const response = await analysis.analyzeFiles(formData);
      
      if (response.data.success) {
        setAnalysisResult(response.data);
        // Refresh user data to update credits
        await refreshUser();
      } else {
        setError(response.data.error);
      }
    } catch (error) {
      if (error.response?.status === 402) {
        setError('Insufficient credits. Please purchase more credits to continue.');
      } else {
        setError(error.response?.data?.error || 'Analysis failed. Please try again.');
      }
    } finally {
      setAnalyzing(false);
    }
  };

  const handleDemoAnalysis = async () => {
    setAnalyzing(true);
    setError('');

    try {
      const response = await analysis.demoAnalysis();
      if (response.data.success) {
        setAnalysisResult(response.data);
      } else {
        setError(response.data.error);
      }
    } catch (error) {
      setError('Demo analysis failed. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };

  const handlePurchaseCredits = async (packageId) => {
    try {
      // For demo purposes, simulate purchase
      const response = await payments.simulatePurchase(packageId);
      if (response.data.success) {
        await refreshUser();
        alert(`Successfully added ${response.data.credits_added} credits!`);
      }
    } catch (error) {
      setError('Purchase failed. Please try again.');
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical': return 'text-red-600 bg-red-50';
      case 'high': return 'text-orange-600 bg-orange-50';
      case 'medium': return 'text-yellow-600 bg-yellow-50';
      case 'low': return 'text-blue-600 bg-blue-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <Code className="h-5 w-5 text-white" />
                </div>
                <span className="text-xl font-bold text-gray-900">LintIQ</span>
              </div>
              <Badge variant="secondary">Dashboard</Badge>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Zap className="h-4 w-4 text-yellow-500" />
                <span className="font-medium">{user?.credits || 0} credits</span>
                {user?.is_pro && <Badge className="bg-purple-100 text-purple-700">Pro</Badge>}
              </div>
              
              <div className="flex items-center space-x-2">
                <User className="h-4 w-4 text-gray-500" />
                <span className="text-sm text-gray-600">{user?.username}</span>
              </div>
              
              <Button variant="outline" size="sm" onClick={handleLogout}>
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Welcome Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Brain className="h-5 w-5 text-purple-600" />
                  Welcome to LintIQ
                </CardTitle>
                <CardDescription>
                  Upload your code files for AI-powered analysis and insights
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{user?.analyses_count || 0}</div>
                    <div className="text-sm text-gray-600">Analyses Run</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">{user?.credits || 0}</div>
                    <div className="text-sm text-gray-600">Credits Remaining</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">
                      {user?.is_pro ? 'Pro' : 'Free'}
                    </div>
                    <div className="text-sm text-gray-600">Account Type</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* File Upload */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Upload className="h-5 w-5 text-blue-600" />
                  Upload Code Files
                </CardTitle>
                <CardDescription>
                  Drag and drop files or click to select. Supports .py, .js, .jsx, .ts, .tsx files
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {error && (
                  <Alert variant="destructive">
                    <AlertTriangle className="h-4 w-4" />
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}

                <div
                  className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors cursor-pointer"
                  onDragOver={handleDragOver}
                  onDrop={handleDrop}
                  onClick={() => document.getElementById('file-input').click()}
                >
                  <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-lg font-medium text-gray-600 mb-2">
                    Drop files here or click to browse
                  </p>
                  <p className="text-sm text-gray-500">
                    Maximum file size: 10MB • Maximum total: 50MB
                  </p>
                  <input
                    id="file-input"
                    type="file"
                    multiple
                    accept=".py,.js,.jsx,.ts,.tsx,.zip"
                    onChange={handleFileSelect}
                    className="hidden"
                  />
                </div>

                {files.length > 0 && (
                  <div className="space-y-2">
                    <h4 className="font-medium">Selected Files:</h4>
                    {files.map((file, index) => (
                      <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                        <div className="flex items-center space-x-2">
                          <FileText className="h-4 w-4 text-blue-600" />
                          <span className="text-sm">{file.name}</span>
                        </div>
                        <span className="text-xs text-gray-500">{formatFileSize(file.size)}</span>
                      </div>
                    ))}
                  </div>
                )}

                <div className="flex gap-4">
                  <Button 
                    onClick={handleAnalyze} 
                    disabled={analyzing || files.length === 0}
                    className="flex-1"
                  >
                    {analyzing ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <Brain className="mr-2 h-4 w-4" />
                        Analyze Code {user?.is_pro ? '(AI)' : '(Basic)'}
                      </>
                    )}
                  </Button>
                  
                  <Button 
                    variant="outline" 
                    onClick={handleDemoAnalysis}
                    disabled={analyzing}
                  >
                    Try Demo
                  </Button>
                </div>

                {!user?.is_pro && (
                  <Alert>
                    <Brain className="h-4 w-4" />
                    <AlertDescription>
                      Upgrade to Pro for AI-powered insights and unlimited analyses.
                    </AlertDescription>
                  </Alert>
                )}
              </CardContent>
            </Card>

            {/* Analysis Results */}
            {analysisResult && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    Analysis Results
                  </CardTitle>
                  <CardDescription>
                    {analysisResult.is_demo ? 'Demo analysis results' : `Analysis of ${analysisResult.files_analyzed} file(s)`}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Tabs defaultValue="summary" className="w-full">
                    <TabsList className="grid w-full grid-cols-3">
                      <TabsTrigger value="summary">Summary</TabsTrigger>
                      <TabsTrigger value="issues">Issues</TabsTrigger>
                      <TabsTrigger value="files">Files</TabsTrigger>
                    </TabsList>
                    
                    <TabsContent value="summary" className="space-y-4">
                      <div className="grid md:grid-cols-2 gap-4">
                        <Card>
                          <CardContent className="pt-6">
                            <div className="text-center">
                              <div className="text-3xl font-bold text-blue-600 mb-2">
                                {analysisResult.summary?.overall_score || 0}/10
                              </div>
                              <div className="text-sm text-gray-600">Overall Score</div>
                            </div>
                          </CardContent>
                        </Card>
                        
                        <Card>
                          <CardContent className="pt-6">
                            <div className="text-center">
                              <div className="text-3xl font-bold text-red-600 mb-2">
                                {analysisResult.total_issues || 0}
                              </div>
                              <div className="text-sm text-gray-600">Total Issues</div>
                            </div>
                          </CardContent>
                        </Card>
                      </div>

                      <div className="grid grid-cols-4 gap-4">
                        <div className="text-center">
                          <div className="text-lg font-bold text-red-600">
                            {analysisResult.summary?.critical_issues || 0}
                          </div>
                          <div className="text-xs text-gray-600">Critical</div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-bold text-orange-600">
                            {analysisResult.summary?.high_issues || 0}
                          </div>
                          <div className="text-xs text-gray-600">High</div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-bold text-yellow-600">
                            {analysisResult.summary?.medium_issues || 0}
                          </div>
                          <div className="text-xs text-gray-600">Medium</div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-bold text-blue-600">
                            {analysisResult.summary?.low_issues || 0}
                          </div>
                          <div className="text-xs text-gray-600">Low</div>
                        </div>
                      </div>

                      {analysisResult.ai_analysis && (
                        <Card className="bg-purple-50 border-purple-200">
                          <CardHeader>
                            <CardTitle className="text-lg flex items-center gap-2">
                              <Brain className="h-5 w-5 text-purple-600" />
                              AI Insights
                            </CardTitle>
                          </CardHeader>
                          <CardContent>
                            <p className="text-gray-700 mb-4">{analysisResult.ai_analysis.summary}</p>
                            {analysisResult.ai_analysis.recommendations?.length > 0 && (
                              <div>
                                <h4 className="font-medium mb-2">Recommendations:</h4>
                                <ul className="space-y-1">
                                  {analysisResult.ai_analysis.recommendations.slice(0, 3).map((rec, index) => (
                                    <li key={index} className="text-sm text-gray-600">• {rec}</li>
                                  ))}
                                </ul>
                              </div>
                            )}
                          </CardContent>
                        </Card>
                      )}
                    </TabsContent>
                    
                    <TabsContent value="issues" className="space-y-4">
                      {analysisResult.analysis_results?.map((fileResult, index) => (
                        <Card key={index}>
                          <CardHeader>
                            <CardTitle className="text-lg">{fileResult.filename}</CardTitle>
                            <CardDescription>
                              {fileResult.language} • {fileResult.issues?.length || 0} issues found
                            </CardDescription>
                          </CardHeader>
                          <CardContent>
                            {fileResult.issues?.length > 0 ? (
                              <div className="space-y-2">
                                {fileResult.issues.slice(0, 5).map((issue, issueIndex) => (
                                  <div key={issueIndex} className="flex items-start space-x-3 p-3 rounded-lg bg-gray-50">
                                    <Badge className={getSeverityColor(issue.severity)}>
                                      {issue.severity}
                                    </Badge>
                                    <div className="flex-1">
                                      <p className="text-sm font-medium">{issue.message}</p>
                                      <p className="text-xs text-gray-500">
                                        Line {issue.line} • {issue.source}
                                      </p>
                                    </div>
                                  </div>
                                ))}
                                {fileResult.issues.length > 5 && (
                                  <p className="text-sm text-gray-500 text-center">
                                    ... and {fileResult.issues.length - 5} more issues
                                  </p>
                                )}
                              </div>
                            ) : (
                              <p className="text-green-600 text-center py-4">No issues found! 🎉</p>
                            )}
                          </CardContent>
                        </Card>
                      ))}
                    </TabsContent>
                    
                    <TabsContent value="files" className="space-y-4">
                      {analysisResult.analysis_results?.map((fileResult, index) => (
                        <Card key={index}>
                          <CardHeader>
                            <CardTitle className="text-lg flex items-center justify-between">
                              {fileResult.filename}
                              <Badge variant="outline">{fileResult.language}</Badge>
                            </CardTitle>
                          </CardHeader>
                          <CardContent>
                            <div className="grid md:grid-cols-3 gap-4">
                              <div className="text-center">
                                <div className="text-lg font-bold text-blue-600">
                                  {fileResult.score || 0}/10
                                </div>
                                <div className="text-xs text-gray-600">Quality Score</div>
                              </div>
                              <div className="text-center">
                                <div className="text-lg font-bold text-gray-600">
                                  {fileResult.metrics?.lines_of_code || 0}
                                </div>
                                <div className="text-xs text-gray-600">Lines of Code</div>
                              </div>
                              <div className="text-center">
                                <div className="text-lg font-bold text-red-600">
                                  {fileResult.issues?.length || 0}
                                </div>
                                <div className="text-xs text-gray-600">Issues Found</div>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </TabsContent>
                  </Tabs>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Account Info */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <User className="h-5 w-5 text-blue-600" />
                  Account
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="text-sm text-gray-600">Username</div>
                  <div className="font-medium">{user?.username}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Email</div>
                  <div className="font-medium">{user?.email}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Plan</div>
                  <div className="flex items-center gap-2">
                    <span className="font-medium">{user?.is_pro ? 'Pro' : 'Free'}</span>
                    {user?.is_pro && <Badge className="bg-purple-100 text-purple-700">Pro</Badge>}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Credits */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Zap className="h-5 w-5 text-yellow-500" />
                  Credits
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-600">{user?.credits || 0}</div>
                  <div className="text-sm text-gray-600">Available Credits</div>
                </div>
                
                {!user?.is_pro && user?.credits < 5 && (
                  <Alert>
                    <AlertTriangle className="h-4 w-4" />
                    <AlertDescription>
                      Running low on credits. Consider upgrading to Pro for unlimited analyses.
                    </AlertDescription>
                  </Alert>
                )}

                <div className="space-y-2">
                  <h4 className="font-medium">Purchase Credits</h4>
                  {loadingPackages ? (
                    <div className="text-center py-4">
                      <Loader2 className="h-6 w-6 animate-spin mx-auto" />
                    </div>
                  ) : (
                    creditPackages.slice(0, 2).map((pkg) => (
                      <Card key={pkg.id} className="p-3">
                        <div className="flex items-center justify-between">
                          <div>
                            <div className="font-medium">{pkg.name}</div>
                            <div className="text-sm text-gray-600">{pkg.price_display}</div>
                          </div>
                          <Button 
                            size="sm" 
                            onClick={() => handlePurchaseCredits(pkg.id)}
                          >
                            Buy
                          </Button>
                        </div>
                      </Card>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Quick Stats */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-green-600" />
                  Quick Stats
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Total Analyses</span>
                  <span className="font-medium">{user?.analyses_count || 0}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Total Spent</span>
                  <span className="font-medium">${((user?.total_spent || 0) / 100).toFixed(2)}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Member Since</span>
                  <span className="font-medium">
                    {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                  </span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

