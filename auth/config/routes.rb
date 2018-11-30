# frozen_string_literal: true

Rails.application.routes.draw do

  #devise_for :users
  devise_for :users, controllers: { sessions: 'users/sessions' }

  devise_scope :user do
    post "/users/sessions/verify_otp" => "users/sessions#verify_otp"

    authenticated :user do
      root 'stuks#index', as: :authenticated_root
    end

    unauthenticated do
      root 'devise/sessions#new', as: :unauthenticated_root
    end
  end

  resources :two_factor do
    collection do
      get :activate
      get :deactivate
    end
  end

  # Front-end
  root to: "stuks#index"

  # API verification
  get 'verify/test', to: 'stuks#verify_test', as: 'verify_test'
  get 'verify/:user_domain_token', to: 'stuks#verify', as: 'verify', defaults: { format: :json }
end
