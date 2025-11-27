import React, { useState, useEffect } from 'react';
import { GoogleLogin, CredentialResponse } from '@react-oauth/google';
import { useAuth } from './AuthContext';
import { authenticateWithGoogle, authenticateWithFacebook } from './grpcClient';

interface FacebookSDK {
  init: (params: any) => void;
  login: (callback: (response: any) => void, params?: any) => void;
  api: (path: string, callback: (response: any) => void) => void;
}

declare global {
  interface Window {
    FB?: FacebookSDK;
    fbAsyncInit?: () => void;
  }
}

const Login: React.FC = () => {
  const { login } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [fbLoaded, setFbLoaded] = useState(false);

  // Load Facebook SDK
  useEffect(() => {
    const fbAppId = import.meta.env.VITE_FACEBOOK_APP_ID;

    if (!fbAppId) {
      console.warn('Facebook App ID not configured');
      return;
    }

    // Initialize Facebook SDK
    window.fbAsyncInit = function() {
      window.FB?.init({
        appId: fbAppId,
        cookie: true,
        xfbml: true,
        version: 'v18.0'
      });
      setFbLoaded(true);
    };

    // Load Facebook SDK script
    if (!document.getElementById('facebook-jssdk')) {
      const script = document.createElement('script');
      script.id = 'facebook-jssdk';
      script.src = 'https://connect.facebook.net/en_US/sdk.js';
      script.async = true;
      script.defer = true;
      document.body.appendChild(script);
    } else {
      setFbLoaded(true);
    }
  }, []);

  const handleGoogleSuccess = async (credentialResponse: CredentialResponse) => {
    if (!credentialResponse.credential) {
      setError('No credential received from Google');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const authResponse = await authenticateWithGoogle(credentialResponse.credential);
      login(authResponse.user, authResponse.token);
    } catch (err) {
      console.error('Google login error:', err);
      setError('Failed to authenticate with Google. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoogleError = () => {
    setError('Google login failed. Please try again.');
  };

  const handleFacebookLogin = () => {
    if (!window.FB) {
      setError('Facebook SDK not loaded. Please refresh and try again.');
      return;
    }

    setIsLoading(true);
    setError(null);

    window.FB.login((response: any) => {
      if (response.authResponse) {
        const { accessToken, userID } = response.authResponse;

        authenticateWithFacebook(accessToken, userID)
          .then((authResponse) => {
            login(authResponse.user, authResponse.token);
          })
          .catch((err) => {
            console.error('Facebook login error:', err);
            setError('Failed to authenticate with Facebook. Please try again.');
          })
          .finally(() => {
            setIsLoading(false);
          });
      } else {
        setError('Facebook login was cancelled.');
        setIsLoading(false);
      }
    }, { scope: 'public_profile,email' });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">SnapTop</h1>
          <p className="text-gray-600">AI-Powered Meal Planning</p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}

        {isLoading && (
          <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-blue-600 text-sm">Authenticating...</p>
          </div>
        )}

        <div className="space-y-4">
          <div className="flex flex-col items-center">
            <p className="text-gray-700 mb-4 font-medium">Sign in to continue</p>

            <div className="mb-4 w-full flex justify-center">
              <GoogleLogin
                onSuccess={handleGoogleSuccess}
                onError={handleGoogleError}
                useOneTap
                theme="outline"
                size="large"
                text="signin_with"
              />
            </div>

            <button
              onClick={handleFacebookLogin}
              disabled={isLoading || !fbLoaded}
              className={`w-full flex items-center justify-center gap-3 px-6 py-3 rounded-lg font-medium transition ${
                isLoading || !fbLoaded
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              }`}
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
              {fbLoaded ? 'Continue with Facebook' : 'Loading Facebook...'}
            </button>
          </div>
        </div>

        <div className="mt-8 text-center">
          <p className="text-sm text-gray-500">
            By signing in, you agree to our Terms of Service and Privacy Policy
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
