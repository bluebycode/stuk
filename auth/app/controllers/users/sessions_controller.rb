class Users::SessionsController < Devise::SessionsController
  def create
    return redirect_to new_user_session_path unless user_exist?
    user = User.find_by(id: session[:temp_user_id])
    return render :otp  if user.otp_required_for_login
    create_session(user)
  end

  def user_exist?
    return false unless user = User.find_by(email: params[:user][:email])
    return false unless user.valid_password?(params[:user][:password])
    session[:temp_user_id] = user.id
    true
  end

  def verify_otp
    user = User.find_by(id: session[:temp_user_id])
    if user.validate_and_consume_otp!(params[:otp_attempt], otp_secret: user.otp_secret)
      create_session(user)
    else
      render :otp
    end
  end

  def create_session(user)
    sign_in(user)
    session.delete(:temp_user_id)
    respond_with user, location: after_sign_in_path_for(user)
  end
end