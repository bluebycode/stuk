# frozen_string_literal: true

Rails.application.routes.draw do
  resources :machines
  devise_for :users, controllers: { sessions: 'users/sessions' }

  devise_scope :user do
    post '/users/sessions/verify_otp' => 'users/sessions#verify_otp'
  end

  resources :stuks do
    collection do
      get :install_gauth
      get :uninstall_gauth
    end
  end

  # Front-end
  root to: 'stuks#index'
  get 'admin_dashboard', to: 'stuks#admin_dashboard', as: 'admin_dashboard'
  get 'generate_config/:id', to: 'stuks#generate_config', as: 'generate_config'
  get 'download_stuk_client/', to: 'stuks#download_stuk_client', as: 'download_stuk_client'
  get 'machine_users/:id', to: 'machines#machine_users', as: 'machine_users'
  post 'assign_user_machine/:id', to: 'machines#assign_user_machine', as: 'assign_user_machine'
  post 'unassign_user_machine/:id', to: 'machines#unassign_user_machine', as: 'unassign_user_machine'

  # API verification
  get 'verify_test/:user_domain_token', to: 'stuks#verify_test', as: 'verify_test', defaults: { format: :json }
  get 'verify/:user_domain_token', to: 'stuks#verify', as: 'verify', defaults: { format: :json }
end
