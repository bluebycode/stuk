require 'test_helper'

class StuksControllerTest < ActionDispatch::IntegrationTest
  setup do
    @stuk = stuks(:one)
  end

  test "should get index" do
    get stuks_url
    assert_response :success
  end

  test "should get new" do
    get new_stuk_url
    assert_response :success
  end

  test "should create stuk" do
    assert_difference('Stuk.count') do
      post stuks_url, params: { stuk: {  } }
    end

    assert_redirected_to stuk_url(Stuk.last)
  end

  test "should show stuk" do
    get stuk_url(@stuk)
    assert_response :success
  end

  test "should get edit" do
    get edit_stuk_url(@stuk)
    assert_response :success
  end

  test "should update stuk" do
    patch stuk_url(@stuk), params: { stuk: {  } }
    assert_redirected_to stuk_url(@stuk)
  end

  test "should destroy stuk" do
    assert_difference('Stuk.count', -1) do
      delete stuk_url(@stuk)
    end

    assert_redirected_to stuks_url
  end
end
