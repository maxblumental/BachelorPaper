if [ -d "bin/" ]; then
  rm -rf bin
fi

if [ -d "images/" ]; then
  rm -rf images
fi

rm *.log *.png 2> /dev/null
