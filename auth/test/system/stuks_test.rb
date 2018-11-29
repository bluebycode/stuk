require "application_system_test_case"

class StuksTest < ApplicationSystemTestCase
  setup do
    @stuk = stuks(:one)
  end

  test "visiting the index" do
    visit stuks_url
    assert_selector "h1", text: "Stuks"
  end

  test "creating a Stuk" do
    visit stuks_url
    click_on "New Stuk"

    click_on "Create Stuk"

    assert_text "Stuk was successfully created"
    click_on "Back"
  end

  test "updating a Stuk" do
    visit stuks_url
    click_on "Edit", match: :first

    click_on "Update Stuk"

    assert_text "Stuk was successfully updated"
    click_on "Back"
  end

  test "destroying a Stuk" do
    visit stuks_url
    page.accept_confirm do
      click_on "Destroy", match: :first
    end

    assert_text "Stuk was successfully destroyed"
  end
end
