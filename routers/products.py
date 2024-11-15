
from fastapi import APIRouter, status, HTTPException
from connection import execute_query
from schemas.CreateProduct import CreateProductDTO
from schemas.UpdateProduct import UpdateProductDTO

productsRouter = APIRouter(prefix="/products",
    tags=["Products"])

@productsRouter.post('/',status_code=status.HTTP_201_CREATED)
async def create_product(createProductDto: CreateProductDTO):
    query = 'INSERT INTO products (name, description, image, price,discount,stock,category) VALUES (%s, %s, %s, %s,%s,%s, %s) RETURNING *'
    params = (createProductDto.name, createProductDto.description, createProductDto.image,
              createProductDto.price,createProductDto.discount,createProductDto.stock,createProductDto.category)
    try:
        products = await execute_query(query, params)
        return products[0]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@productsRouter.get('/getbyId/{product_id}')
async def get_product_by_id(product_id: int):
    query = 'SELECT * FROM products where id = %s'
    params = (product_id,)
    products = await execute_query(query, params)
    if len(products) == 1:
        return products[0]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Does not exist a product with this Id')


@productsRouter.delete('/deletebyId/{product_id}', status_code=status.HTTP_200_OK)
async def delete_product_by_id(product_id: int):
    # Usamos RETURNING para obtener información de la fila eliminada
    query = 'DELETE FROM products WHERE id = %s RETURNING *'
    params = (product_id,)

    # Ejecuta la consulta y captura el producto eliminado
    deleted_product = await execute_query(query, params)

    if deleted_product:
        return {
            "deleted_product": deleted_product[0]  # Información del producto eliminado
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No product found with the specified ID"
        )

@productsRouter.put('/',status_code=status.HTTP_200_OK)
async def update_product(updateProductDto: UpdateProductDTO):
    if updateProductDto.discount is not None:
        if 0 > updateProductDto.discount or updateProductDto.discount > 100:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The discount cannot be less than 0 or greater than 100')
    if updateProductDto.stock is not None:
        if 0 > updateProductDto.stock and updateProductDto.stock is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The stock cannot be less than 0')
    product = await get_product_by_id(updateProductDto.id)
    before_update_product = product
    if updateProductDto.name is None:
        updateProductDto.name = product['name']
    if updateProductDto.description is None:
        updateProductDto.description =product['description']
    if updateProductDto.image is None:
        updateProductDto.image = product['image']
    if updateProductDto.price is None:
        updateProductDto.price =product['price']
    if updateProductDto.discount is None:
        updateProductDto.discount = product['discount']
    if updateProductDto.stock is None:
        updateProductDto.stock = product['stock']
    if updateProductDto.category is None:
        updateProductDto.category = product['category']


    before_update_product.update(**dict(updateProductDto))
    try:
        query = 'UPDATE products SET  name=%s, description=%s, image=%s, price=%s, discount=%s, stock=%s, category=%s  WHERE id = %s RETURNING *'
        params = (
        before_update_product['name'],before_update_product['description'],before_update_product['image'],
        before_update_product['price'],before_update_product['discount'],before_update_product['stock'],before_update_product['category'],before_update_product['id'])
        await execute_query(query, params)
        return before_update_product
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@productsRouter.get('/searchByName/{product_name}', status_code=status.HTTP_200_OK)
async def search_product_by_name(product_name: str):
    # Modifica el parámetro para incluir comodines y hacer la búsqueda parcial
    query = 'SELECT * FROM products WHERE name LIKE %s'
    params = (f"%{product_name}%",)

    # Ejecuta la consulta
    products = await execute_query(query, params)

    # Verifica si se encontraron productos
    if products:
        return products  # Devuelve todos los productos encontrados
    else:
        return []


@productsRouter.get('/searchByCategory/{product_category}', status_code=status.HTTP_200_OK)
async def search_product_by_category(product_category: str):
    # Modifica el parámetro para incluir comodines y hacer la búsqueda parcial
    query = 'SELECT * FROM products WHERE category LIKE %s'
    params = (f"%{product_category}%",)

    # Ejecuta la consulta
    products = await execute_query(query, params)

    # Verifica si se encontraron productos
    if products:
        return products  # Devuelve todos los productos encontrados
    else:
        return []

@productsRouter.get('/searchByPrice/{max_price}', status_code=status.HTTP_200_OK)
async def search_product_by_max_price(max_price: int):
    # Modifica el parámetro para incluir comodines y hacer la búsqueda parcial
    query = 'SELECT * FROM products WHERE price <=  %s'
    params = (max_price,)

    # Ejecuta la consulta
    products = await execute_query(query, params)

    # Verifica si se encontraron productos
    if products:
        return products  # Devuelve todos los productos encontrados
    else:
        return []

@productsRouter.get('/allProducts', status_code=status.HTTP_200_OK)
async def all_products():
    # Modifica el parámetro para incluir comodines y hacer la búsqueda parcial
    query = 'SELECT * FROM products order by discount DESC'
    # Ejecuta la consulta
    products = await execute_query(query)
    return products  # Devuelve todos los productos encontrados
