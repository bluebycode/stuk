class CreateMachines < ActiveRecord::Migration[5.2]
  def change
    create_table :machines do |t|
      t.string :name
      t.string :ip
      t.string :sequence
      t.text :image_src

      t.timestamps
    end
  end
end
