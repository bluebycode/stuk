# frozen_string_literal: true

Rails.application.routes.draw do
  # Front-end
  devise_for :users
  root to: "stuks#index"

  # API verification
  get 'verify/test', to: 'stuks#verify_test', as: 'verify_test'
  get 'verify/:user_domain_token', to: 'stuks#verify', as: 'verify', defaults: { format: :json }
end
