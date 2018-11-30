# frozen_string_literal: true

Rails.application.routes.draw do

  resources :machines
  #devise_for :users
  devise_for :users, controllers: { sessions: 'users/sessions' }

  devise_scope :user do
    post "/users/sessions/verify_otp" => "users/sessions#verify_otp"
  end

  resources :stuks do
    collection do
      get :install_gauth
      get :uninstall_gauth
    end
  end

  # Front-end
  root to: "stuks#index"

  # API verification
  get 'verify/test', to: 'stuks#verify_test', as: 'verify_test'
  get 'verify/:user_domain_token', to: 'stuks#verify', as: 'verify', defaults: { format: :json }
end
