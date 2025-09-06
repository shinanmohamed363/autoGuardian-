import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <nav className="relative z-10 px-6 py-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="text-2xl font-bold text-white">
            AutoGuardian
          </div>
          <div className="space-x-4">
            <Link
              to="/login"
              className="text-white hover:text-blue-200 transition-colors duration-200"
            >
              Sign In
            </Link>
            <Link
              to="/register"
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
            >
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      <section className="relative px-6 py-20">
        <div className="max-w-7xl mx-auto text-center">
          <div className="animate-fade-in">
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
              Transform Your Vehicle Journey with{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">
                AI Intelligence
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-4xl mx-auto">
              From purchase to maintenance, AutoGuardian's AI-powered platform guides you through 
              every automotive decision with confidence and savings.
            </p>
            <div className="space-x-4">
              <Link
                to="/register"
                className="inline-block bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-semibold px-8 py-4 rounded-xl transition-all duration-200 transform hover:scale-105 shadow-lg"
              >
                Start Your Smart Vehicle Journey Today
              </Link>
              <button className="inline-block border border-white/20 hover:border-white/40 text-white font-semibold px-8 py-4 rounded-xl transition-all duration-200 backdrop-blur-sm hover:bg-white/5">
                Watch Demo
              </button>
            </div>
          </div>
        </div>
      </section>

      <section className="px-6 py-20">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-6">Stop Guessing. Start Knowing.</h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Making the right vehicle decision shouldn't take months of research or cost you thousands 
              in hidden expenses. AutoGuardian combines cutting-edge AI with real-world automotive expertise.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all duration-200">
              <div className="text-red-400 text-3xl mb-4">⚠️</div>
              <h3 className="text-xl font-semibold text-white mb-3">The Problem</h3>
              <ul className="text-gray-300 space-y-2">
                <li>• 63% of vehicle buyers experience post-purchase regret</li>
                <li>• Most underestimate ownership costs by 40-60%</li>
                <li>• Traditional research takes 3+ months</li>
                <li>• Hidden expenses average $6,684 annually</li>
              </ul>
            </div>

            <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all duration-200">
              <div className="text-blue-400 text-3xl mb-4">🤖</div>
              <h3 className="text-xl font-semibold text-white mb-3">Our Solution</h3>
              <p className="text-gray-300">
                AutoGuardian eliminates guesswork with AI-powered insights that save you time, 
                money, and stress. Our platform learns your needs and delivers personalized recommendations.
              </p>
            </div>

            <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all duration-200">
              <div className="text-green-400 text-3xl mb-4">✨</div>
              <h3 className="text-xl font-semibold text-white mb-3">Key Benefits</h3>
              <ul className="text-gray-300 space-y-2">
                <li>• Reduce decision time to 1 week</li>
                <li>• Save 20-30% on ownership costs</li>
                <li>• Get 90%+ accurate vehicle matching</li>
                <li>• Predict maintenance needs</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <section className="px-6 py-20 bg-white/5">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-6">Powerful Features</h2>
            <p className="text-xl text-gray-300">Everything you need for intelligent automotive decisions</p>
          </div>

          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <div className="flex items-start space-x-4">
                <div className="bg-blue-600 rounded-lg p-3">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-white mb-2">Intelligent Vehicle Matching</h3>
                  <p className="text-gray-300">Find your perfect vehicle in minutes with our AI that analyzes 15+ decision factors.</p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="bg-green-600 rounded-lg p-3">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-white mb-2">Predictive Analytics</h3>
                  <p className="text-gray-300">85% accurate maintenance predictions and total cost of ownership projections.</p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="bg-purple-600 rounded-lg p-3">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-white mb-2">AI Transaction Support</h3>
                  <p className="text-gray-300">Real-time negotiation assistance with market data integration.</p>
                </div>
              </div>
            </div>

            <div className="relative">
              <div className="bg-gradient-to-br from-blue-600/20 to-purple-600/20 rounded-2xl p-8 border border-white/10">
                <div className="text-center">
                  <div className="text-6xl mb-4">🚗</div>
                  <h3 className="text-2xl font-bold text-white mb-4">Your Smart Vehicle Journey</h3>
                  <div className="space-y-3 text-left">
                    <div className="flex items-center space-x-3">
                      <div className="bg-blue-600 rounded-full w-6 h-6 flex items-center justify-center text-white text-sm">1</div>
                      <span className="text-gray-300">5-minute assessment</span>
                    </div>
                    <div className="flex items-center space-x-3">
                      <div className="bg-blue-600 rounded-full w-6 h-6 flex items-center justify-center text-white text-sm">2</div>
                      <span className="text-gray-300">AI analyzes thousands of vehicles</span>
                    </div>
                    <div className="flex items-center space-x-3">
                      <div className="bg-blue-600 rounded-full w-6 h-6 flex items-center justify-center text-white text-sm">3</div>
                      <span className="text-gray-300">Personalized recommendations</span>
                    </div>
                    <div className="flex items-center space-x-3">
                      <div className="bg-blue-600 rounded-full w-6 h-6 flex items-center justify-center text-white text-sm">4</div>
                      <span className="text-gray-300">Real-time decision support</span>
                    </div>
                    <div className="flex items-center space-x-3">
                      <div className="bg-blue-600 rounded-full w-6 h-6 flex items-center justify-center text-white text-sm">5</div>
                      <span className="text-gray-300">Ongoing optimization</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="px-6 py-20">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-6">Proven Results</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
            <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6">
              <div className="text-3xl font-bold text-blue-400 mb-2">50K+</div>
              <div className="text-gray-300">Vehicle Database Entries</div>
            </div>
            <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6">
              <div className="text-3xl font-bold text-green-400 mb-2">90%+</div>
              <div className="text-gray-300">Recommendation Accuracy</div>
            </div>
            <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6">
              <div className="text-3xl font-bold text-purple-400 mb-2">70%</div>
              <div className="text-gray-300">Decision Time Reduction</div>
            </div>
            <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6">
              <div className="text-3xl font-bold text-yellow-400 mb-2">30%</div>
              <div className="text-gray-300">Cost Savings</div>
            </div>
          </div>

          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-center">
            <h3 className="text-3xl font-bold text-white mb-4">Ready to Transform Your Vehicle Journey?</h3>
            <p className="text-xl text-blue-100 mb-8">
              Join thousands of smart vehicle owners who've discovered the power of AI-driven automotive decisions.
            </p>
            <Link
              to="/register"
              className="inline-block bg-white hover:bg-gray-100 text-blue-600 font-bold px-8 py-4 rounded-xl transition-colors duration-200 transform hover:scale-105"
            >
              Get Started Free
            </Link>
          </div>
        </div>
      </section>

      <footer className="px-6 py-8 border-t border-white/10">
        <div className="max-w-7xl mx-auto text-center">
          <div className="text-2xl font-bold text-white mb-4">AutoGuardian</div>
          <p className="text-gray-400">© 2025 AutoGuardian. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;