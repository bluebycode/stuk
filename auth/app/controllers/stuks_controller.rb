class StuksController < ApplicationController
  before_action :set_stuk, only: [:show, :edit, :update, :destroy]

  def index
    @user = current_user
  end
end
