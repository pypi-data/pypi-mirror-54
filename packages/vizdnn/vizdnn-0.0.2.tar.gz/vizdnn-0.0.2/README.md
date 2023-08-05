# Vizdnn


Interpretable Deep Neural network is the next phase of understanding the working of neural network. This library suffices the need to vizualize neural network layer with simple python pip package. 






### Pip Install

```
pip install vizdnn==0.0.1
```


### Use

```python
import vizdnn
import keras

visualize_neural_network = vizdnn(keras.applications.resnet.ResNet50() , "network_layer_name" , "test_image_name.jpg")

vis_layer = visualize_neural_network.get_layer()
visualize_neural_network.viz_feature_map(vis_layer)

```

### Sample Viz

- Sample test image

![test-image-name.jpg](https://i.postimg.cc/Njnbfjtt/test-image-name.jpg)

<br>

- Vizualization from Resnet50 conv1_bn Layer.


 ![Screenshot-from-2019-10-22-18-43-48.png](https://i.postimg.cc/zXPsm5ym/Screenshot-from-2019-10-22-18-43-48.png)

 <br>


 - Vizualization from VGG16 block2_conv1 Layer.

 ![Screenshot-from-2019-10-22-18-46-14.png](https://i.postimg.cc/KcCWQfwF/Screenshot-from-2019-10-22-18-46-14.png)

 <br>
