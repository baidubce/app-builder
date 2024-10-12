cd ..
find . -name "*.py" -exec sed -i '' 's/@HTTPClient\.check_param/# @HTTPClient.check_param/g' {} \;
cd doc
sh update_doc.sh